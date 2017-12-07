import subprocess

from opinel.utils.console import configPrintException
from opinel.utils.credentials import read_creds_from_environment_variables

#
# Test for Scout2.py
#
class TestScout2Class:

    #
    # Setup
    #
    def setup(self):
        configPrintException(True)
        creds = read_creds_from_environment_variables()
        self.profile_name = 'travislike' if creds['AccessKeyId'] == None else None

    def get_command(self, args):
        command = './Scout2.py'
        if self.profile_name:
            command += ' --profile %s' % self.profile_name
        command += ' %s' % args
        return command

    #
    # Make sure that Scout2 does not crash with --help
    #
    def test_scout2_help(self):
        command = self.get_command('--help')
        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
        process.wait()
        assert process.returncode == 0

    #
    # Make sure that Scout2's default run does not crash
    #
    def test_scout2_default_run(self):
        command = self.get_command('--force --debug')
        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
        process.wait()
        assert process.returncode == 0

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
