# -*- coding: utf-8 -*-

import tempfile
import unittest
from ScoutSuite.core.fs import *
from ScoutSuite.core.console import *


class TestOpinelFsClass(unittest.TestCase):
    """
    Test opinel.fs
    """

    def cmp(self, a, b):
        """
        Implement cmp() for Python3 tests
        """
        return (a > b) - (a < b)

    def test_CustomJSONEncoder(self):
        date = datetime.datetime(2017, 6, 12)
        blob1 = {'foo': 'bar', 'date': date}
        print('%s' % json.dumps(blob1, cls=CustomJSONEncoder))
        blob2 = {'foo': 'bar', 'baz': {'foo': 'bar'}}
        print('%s' % json.dumps(blob2, cls=CustomJSONEncoder))

    def test_load_data(self):
        test = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/protocols.json')
        load_data(test, local_file=True)
        load_data(test, 'protocols', local_file=True)
        load_data('protocols.json', 'protocols')
        load_data('aws/ip-ranges/aws.json', 'prefixes')
        load_data('tests/data/protocols.json', 'protocols', local_file=True)
        test = load_data('protocols.json', 'protocols')
        assert type(test) == dict
        assert test['1'] == 'ICMP'
        test = load_data('tests/data/protocols.json', 'protocols', True)
        assert type(test) == dict
        assert test['-2'] == 'TEST'

    def test_read_ip_ranges(self):
        read_ip_ranges('aws/ip-ranges/aws.json', local_file=False)
        read_ip_ranges('tests/data/ip-ranges-1.json', local_file=True)
        read_ip_ranges('tests/data/ip-ranges-1.json', local_file=True, ip_only=True)

        # Each case's golden `results` file was verified to be the actual,
        # exact return value of read_ip_ranges() called with that case's
        # params (order-independent dict comparison, since read_ip_ranges
        # preserves list order but dict key order is irrelevant).
        #
        # Two other cases that used to sit in this table were investigated
        # and found to be genuinely broken, not just uniterated -- excluded
        # here rather than forced to pass:
        #   - An 'aws.json' case (local_file=False, filtering on
        #     ip_prefix == '23.20.0.0/14'): after fixing its filename typo
        #     ('tests/aws/ip-ranges/aws.json' -> 'aws/ip-ranges/aws.json',
        #     matching the working call on the first line of this test), it
        #     runs, but the bundled ScoutSuite/data/aws/ip-ranges/aws.json
        #     now includes a 'network_border_group' field that the golden
        #     file tests/results/read_ip_ranges/ip-ranges-a.json does not
        #     have -- the golden fixture is stale relative to that bundled
        #     (real, periodically-refreshed AWS) data file. Not a code bug;
        #     needs a human decision on whether to regenerate the golden
        #     file or stop asserting exact equality against live AWS data.
        #   - An 'ip-ranges-3.json' case (also duplicated under a second,
        #     differently-pathed entry with the same broken result): that
        #     file's own `source` field points at tests/data/ip-ranges-2.json,
        #     which does not exist anywhere in this repo, so the case cannot
        #     run at all. Missing fixture, not something to fabricate here.
        test_cases = [
            {
                'filename': 'tests/data/ip-ranges-1.json',
                'local_file': True,
                'conditions': [], 'ip_only': False,
                'results': 'tests/results/read_ip_ranges/ip-ranges-1a.json'
            },
            {
                'filename': 'tests/data/ip-ranges-1.json',
                'local_file': True,
                'conditions': [], 'ip_only': True,
                'results': 'tests/results/read_ip_ranges/ip-ranges-1b.json'
            },
            {
                'filename': 'tests/data/ip-ranges-1.json',
                'local_file': True,
                'conditions': [
                    [
                        'field_a', 'equal', 'a1']],
                'ip_only': True,
                'results': 'tests/results/read_ip_ranges/ip-ranges-1c.json'
            },
        ]

        for case in test_cases:
            actual = read_ip_ranges(case['filename'], local_file=case['local_file'],
                                    ip_only=case['ip_only'], conditions=case['conditions'])
            with open(case['results']) as f:
                expected = json.load(f)
            assert actual == expected

    def test_save_blob_as_json(self):
        date = datetime.datetime.now()
        save_blob_as_json('tmp1.json', {'foo': 'bar', 'date': date}, True)
        save_blob_as_json('tmp1.json', {'foo': 'bar'}, True)
        save_blob_as_json('/root/tmp1.json', {'foo': 'bar'}, True)

        # Regression test: save_blob_as_json's docstring promises it writes
        # the blob to `filename` as JSON, but it used to only print_info() the
        # computed JSON string and never write it to the opened file handle.
        # Since this function has no other caller, nothing else would catch
        # that regression -- assert the file actually contains the blob.
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = os.path.join(tmp_dir, 'blob.json')
            blob = {'foo': 'bar', 'count': 3, 'nested': {'a': 1}}
            save_blob_as_json(target, blob, True)

            assert os.path.exists(target)
            with open(target) as f:
                written = json.load(f)
            assert written == blob
