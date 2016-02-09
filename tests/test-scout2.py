import subprocess

#
# Test for Scout2.py
#
class TestScout2Class:

    #
    # Make sure that Scout2 does not crash with --help
    #
    def test_scout2_help(self):
        command = './Scout2.py --help'
        process = subprocess.Popen(command, shell=True, stdout=None) #subprocess.PIPE)
        process.wait()
        assert process.returncode == 0

    #
    # Make sure that Scout2's default run does not crash
    #
    def test_scout2_default_run(self):
        command = './Scout2.py --force --debug'
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
