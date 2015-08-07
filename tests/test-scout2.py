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
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0

    #
    # Make sure that Scout2's default run does not crash
    #
    def test_scout2_default_run(self):
        command = './Scout2.py --force'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0
