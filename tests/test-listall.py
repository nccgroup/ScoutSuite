import subprocess

#
# Tests for ListAll.py
#
class TestListAllClass:  

    #
    # Make sure that ListAll does not crash with --help
    #
    def test_listall_help(self):
        command = './ListAll.py --help'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0
