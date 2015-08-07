import subprocess

#
# Tests for ListItems.py
#
class TestListItemsClass:  

    #
    # Make sure that ListItems does not crash with --help
    #
    def test_listitems_help(self):
        command = './ListItems.py --help'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert process.returncode == 0
