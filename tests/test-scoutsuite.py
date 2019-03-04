import subprocess

import mock
from nose.plugins.attrib import attr

from ScoutSuite.providers.aws.credentials import read_creds_from_environment_variables

from ScoutSuite.__main__ import *


#
# Test for Scout.py
#
class TestScoutSuiteClass:

    @classmethod
    def setUpClass(cls):
        config_debug_level(True)
        creds = read_creds_from_environment_variables()
        cls.profile_name = 'travislike' if creds['AccessKeyId'] == None else None
        cls.has_run_scout_suite = False

    def call_scout_suite(self, args):
        args = ['./Scout.py'] + args

        args.append('aws')

        if TestScoutSuiteClass.profile_name:
            args.append('--profile')
            args.append(TestScoutSuiteClass.profile_name)
        #FIXME this only tests AWS

        args.append('--force')
        args.append('--debug')
        args.append('--no-browser')
        if TestScoutSuiteClass.has_run_scout_suite:
            args.append('--local')
        TestScoutSuiteClass.has_run_scout_suite = True

        with mock.patch.object(sys, 'argv', args):
            return main()

    #
    # Make sure that ScoutSuite does not crash with --help
    #
    def test_scout_suite_help(self):
        command = './Scout.py --help'
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

#    #
#    # Make sure that ScoutSuite's check-s3-acl option does not crash
#    #
#    def test_scout_suite_default_run(self):
#        command = './Scout.py --force --services s3 --check-s3-acls --bucket-name misconfigured-bucket-objectacls-mismatch'
#        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
#        process.wait()
#        assert process.returncode == 0
#
#    #
#    # Make sure that ScoutSuite's check-s3-encryption option does not crash
#    #
#    def test_scout_suite_default_run(self):
#        command = './Scout.py --force --services s3 --check-s3-encryption --bucket-name misconfigured-bucket-unencrypted-objects'
#        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
#        process.wait()
#        assert process.returncode == 0
