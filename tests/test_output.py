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

    def test_html_report(self):
        test_html = HTMLReport(report_name='test')
        assert (test_html.report_name == 'test')
        assert ('json' in test_html.get_content_from_folder(templates_type='conditionals'))
        assert ('json' in test_html.get_content_from_file(filename='/json_format.html'))

    def test_get_filename(self):
        assert ('scoutsuite-report/report.html' in get_filename("REPORT"))
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_results.js' in get_filename("RESULTS"))
        assert ('scoutsuite-results/scoutsuite_results.js' in get_filename("RESULTS", relative_path=True))
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_exceptions.js' in get_filename("EXCEPTIONS"))
        assert ('scoutsuite-results/scoutsuite_exceptions.js' in get_filename("EXCEPTIONS", relative_path=True))
        assert ('scoutsuite-report/scoutsuite-results/scoutsuite_errors.json' in get_filename("ERRORS"))
        assert ('scoutsuite-results/scoutsuite_errors.json' in get_filename("ERRORS", relative_path=True))
