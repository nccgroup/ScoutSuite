import mock
import subprocess

from AWSScout2.__main__ import *

from opinel.utils.console import configPrintException
from opinel.utils.credentials import read_creds_from_environment_variables

#
# Test for Scout2.py
#
class TestScout2Class:

    @classmethod
    def setUpClass(cls):
        configPrintException(True)
        creds = read_creds_from_environment_variables()
        cls.profile_name = 'travislike' if creds['AccessKeyId'] == None else None
        cls.has_run_scout2 = False

    def call_scout2(self, args):
        args = ['./Scout2.py' ] + args
        if TestScout2Class.profile_name:
            args.append('--profile')
            args.append(TestScout2Class.profile_name)
        args.append('--force')
        args.append('--debug')
        args.append('--no-browser')
        if TestScout2Class.has_run_scout2:
            args.append('--local')
        TestScout2Class.has_run_scout2 = True

        with mock.patch.object(sys, 'argv', args):
            return main()


    #
    # Make sure that Scout2 does not crash with --help
    #
    def test_scout2_help(self):
        command = './Scout2.py --help'
        process = subprocess.Popen(command, shell=True, stdout=None)
        process.wait()
        assert process.returncode == 0


    #
    # Make sure that Scout2's default run does not crash
    #
    def test_scout2_default_run(self):
        rc = self.call_scout2([])
        assert (rc == 0)


    #
    # Make sure that Scout2's CIS ruleset run does not crash
    #
    def test_scout2_cis_ruleset_run(self):
        rc = self.call_scout2(['--ruleset', 'cis-02-29-2016.json'])
        assert (rc == 0)


#    #
#    # Make sure that Scout2's check-s3-acl option does not crash
#    #
#    def test_scout2_default_run(self):
#        command = './Scout2.py --force --services s3 --check-s3-acls --bucket-name misconfigured-bucket-objectacls-mismatch'
#        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
#        process.wait()
#        assert process.returncode == 0
#
#    #
#    # Make sure that Scout2's check-s3-encryption option does not crash
#    #
#    def test_scout2_default_run(self):
#        command = './Scout2.py --force --services s3 --check-s3-encryption --bucket-name misconfigured-bucket-unencrypted-objects'
#        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
#        process.wait()
#        assert process.returncode == 0
