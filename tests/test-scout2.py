import subprocess

#
# Test for Scout2.py
#
class TestScout2Class:

    #
    # Make sure that Scout2 does not crash with --help
    #
    def test_listall_help(self):
        command = './RulesGenerator.py --help'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0

    #
    # Make sure that Scout2's default run does not crash
    #
    def test_scout2(self):
        command = './Scout2.py --force --ruleset-name isecpartners --profile isecpartners'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0
