# Import AWS utils
from ScoutSuite.providers.aws.utils import get_keys, no_camel
from ScoutSuite.utils import *


#
# Test methods for ScoutSuite/utils.py
#
class TestScoutUtilsClass:

    def test_format_service_name(self):
        assert (format_service_name('iAm') == 'IAM')
        assert (format_service_name('cloudformation') == 'CloudFormation')

    def test_get_keys(self):
        test1 = {'a': 'b', 'c': 'd'}
        test2 = {'a': '', 'e': 'f'}
        get_keys(test1, test2, 'a')
        assert (test2['a'] == 'b')
        assert ('c' not in test2)
        get_keys(test1, test2, 'c')
        assert (test2['c'] == 'd')

    def test_no_camel(self):
        assert (no_camel('TestTest') == 'test_test')

    def test_is_throttled(self):
        pass
