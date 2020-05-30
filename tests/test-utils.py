# Import AWS utils
from ScoutSuite.providers.aws.utils import (
    get_keys,
    no_camel,
    get_name,
    is_throttled,
    get_aws_account_id,
    get_partition_name,
)
from ScoutSuite.utils import *
import collections
import mock
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
        CustomException = collections.namedtuple("CustomException", "response")
        # test the throttling cases
        for t in ["Throttling", "RequestLimitExceeded", "ThrottlingException"]:
            e = CustomException(response={"Error": {"Code": t}})
            assert is_throttled(e)
        # test the non-throttling exception
        e = CustomException(response={"Error": {"Code": "Not Throttling"}})
        assert not is_throttled(e)
        # test the except block
        e = CustomException(response={"Error": ""})
        assert not is_throttled(e)

    def test_get_name(self):
        src = {
            "Tags": [
                {"Key": "Not Name", "Value": "xyz"},
                {"Key": "Name", "Value": "abc"},
            ],
            "default_attribute": "default_value",
        }
        dst = {}
        default_attribute = "default_attribute"
        assert get_name(src, dst, default_attribute) == "abc"
        assert dst["name"] == "abc"

        src = {
            "Tags": [{"Key": "Not Name", "Value": "xyz"}],
            "default_attribute": "default_value",
        }
        dst = {}
        default_attribute = "default_attribute"
        assert get_name(src, dst, default_attribute) == "default_value"
        assert dst["name"] == "default_value"

    def test_get_identity(self):
        with mock.patch(
            "ScoutSuite.providers.aws.utils.get_caller_identity",
            return_value={"Arn": "a:b:c:d:e:f:"},
        ):
            assert get_aws_account_id("") == "e"

    def test_get_partition_name(self):
        with mock.patch(
            "ScoutSuite.providers.aws.utils.get_caller_identity",
            return_value={"Arn": "a:b:c:d:e:f:"},
        ):
            assert get_partition_name("") == "b"
