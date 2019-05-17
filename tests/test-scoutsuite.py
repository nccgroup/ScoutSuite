import subprocess
import mock

from nose.plugins.attrib import attr
from ScoutSuite.__main__ import run_from_cli
from ScoutSuite.core.console import set_logger_configuration


class TestScoutSuiteClass:

    @classmethod
    def setUpClass(cls):
        set_logger_configuration(is_debug=True)
        cls.has_run_scout_suite = False

    @staticmethod
    def call_scout_suite(args):
        args = ['./scout.py'] + args

        args.append('aws')

        if TestScoutSuiteClass.profile_name:
            args.append('--profile')
            args.append(TestScoutSuiteClass.profile_name)
        # TODO: FIXME this only tests AWS

        args.append('--force')
        args.append('--debug')
        args.append('--no-browser')
        if TestScoutSuiteClass.has_run_scout_suite:
            args.append('--local')
        TestScoutSuiteClass.has_run_scout_suite = True

        sys = None
        with mock.patch.object(sys, 'argv', args):
            return run_from_cli()

    #
    # Make sure that ScoutSuite does not crash with --help
    #
    def test_scout_suite_help(self):
        command = './scout.py --help'
        process = subprocess.Popen(command, shell=True, stdout=None)
        process.wait()
        assert process.returncode == 0

    #
    # Make sure that ScoutSuite's default run does not crash
    #
    @attr("credential")
    def test_scout_suite_default_run(self):
        rc = self.call_scout_suite([])
        assert (rc == 0)

    #
    # Make sure that ScoutSuite's CIS ruleset run does not crash
    #
    @attr("credential")
    def test_scout_suite_cis_ruleset_run(self):
        rc = self.call_scout_suite(['--ruleset', 'cis-02-29-2016.json'])
        assert (rc == 0)
