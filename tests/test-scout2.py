import subprocess

#
# Test methods to make sure that Scout2 as a whole runs
#
class TestScout2Class:  

    #
    # Rough high-level test: make sure that Scout2 does not crash
    #
    def test_scout2(self):
        scout2_command = './Scout2.py --force'
        process = subprocess.Popen(scout2_command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0
