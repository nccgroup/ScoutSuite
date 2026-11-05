"""Tests for ScoutSuite/output/result_encoder.py.

A report file written by ``JavaScriptEncoder`` is also the input of a later
offline re-analysis, so a save that fails must never destroy the report that is
already on disk.

The tests below drive the real encoder, the real filesystem and the real
overwrite prompt. Only the I/O boundary that is being simulated is replaced: a
disk that fills up after a short prefix, a rename that fails, an interrupt, and
the two stdin answers of the overwrite prompt.
"""

import builtins
import datetime
import errno
import json
import os
import shutil
import stat
import tempfile
import unittest
from unittest import mock

from ScoutSuite.output.result_encoder import JavaScriptEncoder, ScoutJsonEncoder
from ScoutSuite.output.utils import get_filename

FILE_TYPES = ('RESULTS', 'EXCEPTIONS', 'ERRORS')

SENTINEL = {'report': 'previous', 'values': [1, 2, 3]}

NEW_CONTENT = {'report': 'new', 'values': [], 'generated': datetime.datetime(2020, 1, 2, 3, 4, 5)}

PREFIX_BYTES = 20


class FailingWriteHandle:
    """A real file handle that stores a short prefix and then fails.

    This is the boundary a full disk shows up at: the first write stores a few
    bytes and the next one raises. The handle itself is a real file on disk.
    """

    def __init__(self, handle, exception, prefix_bytes):
        self._handle = handle
        self._exception = exception
        self._prefix_bytes = prefix_bytes
        self._failed = False

    def write(self, data):
        if self._failed:
            raise self._exception
        self._failed = True
        if self._prefix_bytes:
            self._handle.write(data[:self._prefix_bytes])
            self._handle.flush()
        raise self._exception

    def __getattr__(self, name):
        return getattr(self._handle, name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._handle.close()
        return False


class WriteFault:
    """Context manager failing every write opened inside a directory."""

    def __init__(self, directory, exception, prefix_bytes=PREFIX_BYTES):
        self._directory = os.path.abspath(directory)
        self._exception = exception
        self._prefix_bytes = prefix_bytes
        self.triggered = False
        self._real_open = None
        self._patch = None

    def __enter__(self):
        self._real_open = builtins.open
        fault = self

        def failing_open(file, mode='r', *args, **kwargs):
            handle = fault._real_open(file, mode, *args, **kwargs)
            if isinstance(file, str) and 'w' in mode:
                if os.path.dirname(os.path.abspath(file)) == fault._directory:
                    fault.triggered = True
                    return FailingWriteHandle(handle, fault._exception, fault._prefix_bytes)
            return handle

        self._patch = mock.patch('builtins.open', side_effect=failing_open)
        self._patch.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._patch.stop()
        return False


class JavaScriptEncoderSaveTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='scoutsuite-encoder-')
        self.results_dir = os.path.join(self.temp_dir, 'scoutsuite-results')
        os.makedirs(self.results_dir)
        self.encoder = JavaScriptEncoder(report_name='unit', report_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def report_path(self, file_type):
        path, _ = get_filename(file_type, self.encoder.report_name, self.temp_dir)
        return path

    def expected_text(self, file_type, content, debug=False):
        _, first_line = get_filename(file_type, self.encoder.report_name, self.temp_dir)
        payload = json.dumps(content, indent=4 if debug else None, separators=(',', ': '),
                             sort_keys=True, cls=ScoutJsonEncoder)
        lines = ['%s' % first_line] if first_line else []
        lines.append(payload)
        return '\n'.join(lines) + '\n'

    def expected_loaded(self, file_type, content):
        text = self.expected_text(file_type, content)
        _, first_line = get_filename(file_type, self.encoder.report_name, self.temp_dir)
        if first_line:
            text = text[text.index('\n') + 1:]
        return json.loads(text)

    def write_report(self, file_type, content=SENTINEL):
        path = self.report_path(file_type)
        with open(path, 'w', encoding='utf-8', newline='') as handle:
            handle.write(self.expected_text(file_type, content))
        return path

    def read_bytes(self, path):
        with open(path, 'rb') as handle:
            return handle.read()

    def read_text(self, path):
        # Universal newlines: the file is written in text mode, so the platform
        # line separator is an implementation detail, not part of the format.
        with open(path, encoding='utf-8') as handle:
            return handle.read()

    def unexpected_entries(self):
        expected = {os.path.basename(self.report_path(file_type)) for file_type in FILE_TYPES}
        return sorted(name for name in os.listdir(self.results_dir) if name not in expected)

    @staticmethod
    def circular_content():
        loop = []
        loop.append(loop)
        return {'report': 'circular', 'loop': loop}

    ########################################
    # Successful saves keep the historical format
    ########################################

    def test_creates_new_report_for_each_file_type(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.report_path(file_type)
                self.assertFalse(os.path.exists(path))

                self.encoder.save_to_file(NEW_CONTENT, file_type, force_write=False, debug=False)

                self.assertTrue(os.path.exists(path))
                text = self.read_text(path)
                self.assertEqual(self.expected_text(file_type, NEW_CONTENT), text)
                self.assertTrue(text.endswith('\n'))
                self.assertEqual(self.expected_loaded(file_type, NEW_CONTENT),
                                 self.encoder.load_from_file(file_type))
                self.assertEqual([], self.unexpected_entries())

    def test_replaces_existing_report_when_forced(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.write_report(file_type)
                self.encoder.save_to_file(NEW_CONTENT, file_type, force_write=True, debug=False)

                self.assertEqual(self.expected_text(file_type, NEW_CONTENT), self.read_text(path))
                self.assertEqual(self.expected_loaded(file_type, NEW_CONTENT),
                                 self.encoder.load_from_file(file_type))
                self.assertEqual([], self.unexpected_entries())

    def test_debug_output_keeps_indentation(self):
        self.encoder.save_to_file(NEW_CONTENT, 'RESULTS', force_write=True, debug=True)

        text = self.read_text(self.report_path('RESULTS'))
        self.assertEqual(self.expected_text('RESULTS', NEW_CONTENT, debug=True), text)
        self.assertIn('\n    "', text)
        self.assertEqual(self.expected_loaded('RESULTS', NEW_CONTENT), self.encoder.load_from_file('RESULTS'))

    ########################################
    # A refused overwrite leaves the report alone
    ########################################

    def test_declined_overwrite_keeps_previous_report(self):
        path = self.write_report('RESULTS')
        before = self.read_bytes(path)

        with mock.patch('builtins.input', return_value='n') as asked:
            self.encoder.save_to_file(NEW_CONTENT, 'RESULTS', force_write=False, debug=False)

        self.assertEqual(1, asked.call_count)
        self.assertEqual(before, self.read_bytes(path))
        self.assertEqual(self.expected_loaded('RESULTS', SENTINEL), self.encoder.load_from_file('RESULTS'))
        self.assertEqual([], self.unexpected_entries())

    ########################################
    # Failures must not destroy the report already on disk
    ########################################

    def test_serialization_failure_keeps_previous_report(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.write_report(file_type)
                before = self.read_bytes(path)

                self.encoder.save_to_file(self.circular_content(), file_type, force_write=True, debug=False)

                self.assertEqual(before, self.read_bytes(path))
                self.assertEqual(self.expected_loaded(file_type, SENTINEL),
                                 self.encoder.load_from_file(file_type))
                self.assertEqual([], self.unexpected_entries())

    def test_serialization_failure_creates_no_report(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.report_path(file_type)

                self.encoder.save_to_file(self.circular_content(), file_type, force_write=True, debug=False)

                self.assertFalse(os.path.exists(path))
                self.assertEqual([], self.unexpected_entries())

    def test_write_failure_keeps_previous_report(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.write_report(file_type)
                before = self.read_bytes(path)

                fault = WriteFault(self.results_dir, OSError(errno.ENOSPC, 'No space left on device'))
                with fault:
                    self.encoder.save_to_file(NEW_CONTENT, file_type, force_write=True, debug=False)

                self.assertTrue(fault.triggered, 'the write fault was never exercised')
                self.assertEqual(before, self.read_bytes(path))
                self.assertEqual(self.expected_loaded(file_type, SENTINEL),
                                 self.encoder.load_from_file(file_type))
                self.assertEqual([], self.unexpected_entries())

    def test_replace_failure_keeps_previous_report(self):
        for file_type in FILE_TYPES:
            with self.subTest(file_type=file_type):
                path = self.write_report(file_type)
                before = self.read_bytes(path)
                failure = OSError(errno.EACCES, 'Cannot replace report file')

                with mock.patch('os.replace', side_effect=failure):
                    self.encoder.save_to_file(NEW_CONTENT, file_type, force_write=True, debug=False)

                self.assertEqual(before, self.read_bytes(path))
                self.assertEqual(self.expected_loaded(file_type, SENTINEL),
                                 self.encoder.load_from_file(file_type))
                self.assertEqual([], self.unexpected_entries())

    def test_interrupt_during_write_keeps_previous_report(self):
        path = self.write_report('RESULTS')
        before = self.read_bytes(path)

        fault = WriteFault(self.results_dir, KeyboardInterrupt())
        with fault:
            with self.assertRaises(KeyboardInterrupt):
                self.encoder.save_to_file(NEW_CONTENT, 'RESULTS', force_write=True, debug=False)

        self.assertTrue(fault.triggered, 'the write fault was never exercised')
        self.assertEqual(before, self.read_bytes(path))
        self.assertEqual(self.expected_loaded('RESULTS', SENTINEL), self.encoder.load_from_file('RESULTS'))
        self.assertEqual([], self.unexpected_entries())

    ########################################
    # File metadata
    ########################################

    @unittest.skipUnless(os.name == 'posix', 'POSIX permission and symlink semantics')
    def test_preserves_permissions_of_replaced_report(self):
        path = self.write_report('RESULTS')
        os.chmod(path, 0o640)

        self.encoder.save_to_file(NEW_CONTENT, 'RESULTS', force_write=True, debug=False)

        self.assertEqual(0o640, stat.S_IMODE(os.stat(path).st_mode))

    @unittest.skipUnless(os.name == 'posix', 'POSIX permission and symlink semantics')
    def test_updates_symlink_target(self):
        real_path = os.path.join(self.temp_dir, 'linked-results.js')
        with open(real_path, 'w', encoding='utf-8', newline='') as handle:
            handle.write(self.expected_text('RESULTS', SENTINEL))
        path = self.report_path('RESULTS')
        os.symlink(os.path.relpath(real_path, self.results_dir), path)

        self.encoder.save_to_file(NEW_CONTENT, 'RESULTS', force_write=True, debug=False)

        self.assertTrue(os.path.islink(path), 'the report symlink was replaced instead of its target')
        self.assertEqual(self.expected_text('RESULTS', NEW_CONTENT), self.read_text(real_path))


if __name__ == '__main__':
    unittest.main()
