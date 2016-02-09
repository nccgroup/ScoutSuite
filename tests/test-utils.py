# Import AWS utils
from AWSScout2.utils import *


#
# Test methods for AWSScout2/utils.py
#
class TestAWSScout2UtilsClass:

    #
    # Unit tests for get_scout2_paths
    #
    def test_get_scout2_paths(self):
        assert type(get_scout2_paths('')) == tuple
        assert get_scout2_paths('default') == ('report.html', AWSCONFIG_DIR + '/' + AWSCONFIG_FILE + '.js')
        assert get_scout2_paths('test') == ('report-test.html', AWSCONFIG_DIR + '/' + AWSCONFIG_FILE + '-test.js')
