# Import AWS utils
from AWSScout2.utils import *


#
# Test methods for AWSScout2/utils.py
#
class TestAWSScout2UtilsClass:

    def test_format_service_name(self):
        assert (format_service_name('iAm') == 'IAM')
        assert (format_service_name('cloudformation') == 'CloudFormation')


    def test_get_keys(self):
        test1 = {'a': 'b', 'c': 'd'}
        test2 = {'a': '',  'e': 'f'}
        get_keys(test1, test2, 'a')
        assert (test2['a'] == 'b')
        assert ('c' not in test2)
        get_keys(test1, test2, 'c')
        assert (test2['c'] == 'd')


    def test_no_camel(self):
        assert (no_camel('TestTest') == 'test_test')


    def test_is_throttled(self):
        pass
