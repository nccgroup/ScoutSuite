import unittest
from ScoutSuite.output.html import *
from ScoutSuite.output.utils import *

#
# Test methods for ScoutSuite/output
#
class TestScoutOutput(unittest.TestCase):

    ########################################
    # html.py
    ########################################

    def test_get_filename(self):
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_results.json' in get_filename("RESULTS"))
        assert ('scoutsuite-results/scoutsuite_results.json' in get_filename("RESULTS", relative_path=True))
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_exceptions.json' in get_filename("EXCEPTIONS"))
        assert ('scoutsuite-results/scoutsuite_exceptions.json' in get_filename("EXCEPTIONS", relative_path=True))
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_errors.json' in get_filename("ERRORS"))
        assert ('scoutsuite-results/scoutsuite_errors.json' in get_filename("ERRORS", relative_path=True))
