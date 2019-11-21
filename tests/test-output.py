from ScoutSuite.output.html import *

#
# Test methods for ScoutSuite/output
#
class TestScoutOutput:

    ########################################
    # html.py
    ########################################

    def test_html_report(self):
        test_html = HTMLReport(report_name='test')
        assert (test_html.report_name == 'test')
        assert ('json' in test_html.get_content_from_folder(templates_type='conditionals'))
        assert ('json' in test_html.get_content_from_file(filename='/json_format.html'))