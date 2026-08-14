# -*- coding: utf-8 -*-
import os
import unittest


from ScoutSuite.core.conditions import *


class TestOpinelConditionClass(unittest.TestCase):
    """
    Test opinel.condition
    """

    def test___prepare_age_test(self):
        pass

    def test_pass_condition(self):

        assert pass_condition('a', 'equal', 'a')
        assert pass_condition('a', 'equal', 'b') == False
        assert pass_condition(1, 'equal', 1)
        assert pass_condition(1, 'equal', 0) == False
        assert pass_condition(('a', 'b'), 'equal', ('a', 'b'))
        assert pass_condition(('a', 'b'), 'equal', ('b', 'a')) == False
        assert pass_condition('a', 'notEqual', 'a') == False
        assert pass_condition('a', 'notEqual', 'b')
        assert pass_condition(1, 'notEqual', 1) == False
        assert pass_condition(1, 'notEqual', 0)
        assert pass_condition(('a', 'b'), 'notEqual', ('a', 'b')) == False
        assert pass_condition(('a', 'b'), 'notEqual', ('b', 'a'))

        assert pass_condition(1, 'lessThan', 2)
        assert pass_condition(1, 'lessThan', 1) == False
        assert pass_condition(2, 'lessThan', 1) == False
        assert pass_condition(1, 'lessOrEqual', 2)
        assert pass_condition(1, 'lessOrEqual', 1)
        assert pass_condition(2, 'lessOrEqual', 1) == False
        assert pass_condition(1, 'moreThan', 2) == False
        assert pass_condition(1, 'moreThan', 1) == False
        assert pass_condition(2, 'moreThan', 1)
        assert pass_condition(1, 'moreOrEqual', 2) == False
        assert pass_condition(1, 'moreOrEqual', 1)
        assert pass_condition(2, 'moreOrEqual', 1)

        assert pass_condition({}, 'empty', '')
        assert pass_condition({'a': 'b'}, 'empty', '') == False
        assert pass_condition([], 'empty', '')
        assert pass_condition([None], 'empty', '')
        assert pass_condition(['a'], 'empty', '') == False
        assert pass_condition({}, 'notEmpty', '') == False
        assert pass_condition({'a': 'b'}, 'notEmpty', '')
        assert pass_condition([], 'notEmpty', '') == False
        assert pass_condition([None], 'notEmpty', '') == False
        assert pass_condition(['a'], 'notEmpty', '')
        assert pass_condition(None, 'null', '')
        assert pass_condition('None', 'null', '')
        assert pass_condition(None, 'notNull', '') == False
        assert pass_condition('None', 'notNull', '') == False

        assert pass_condition(True, 'true', '')
        assert pass_condition('TrUE', 'true', '')
        assert pass_condition(False, 'false', '')
        assert pass_condition('FaLSe', 'notTrue', '')

        test_list1 = []
        test_dict1 = {}
        test_list2 = [
            'a']
        test_dict2 = {'a': 'b'}
        test_list3 = ['a', 'b']
        test_dict3 = {'a': 'b', 'c': 'd'}
        assert pass_condition(test_list1, 'lengthLessThan', 1)
        assert pass_condition(test_list1, 'lengthMoreThan', 1) == False
        assert pass_condition(test_list1, 'lengthEqual', 1) == False
        assert pass_condition(test_list2, 'lengthLessThan', 1) == False
        assert pass_condition(test_list2, 'lengthMoreThan', 1) == False
        assert pass_condition(test_list2, 'lengthEqual', 1)
        assert pass_condition(test_list3, 'lengthLessThan', 1) == False
        assert pass_condition(test_list3, 'lengthMoreThan', 1)
        assert pass_condition(test_list3, 'lengthEqual', 1) == False
        assert pass_condition(test_dict1, 'lengthLessThan', 1)
        assert pass_condition(test_dict1, 'lengthMoreThan', 1) == False
        assert pass_condition(test_dict1, 'lengthEqual', 1) == False
        assert pass_condition(test_dict2, 'lengthLessThan', 1) == False
        assert pass_condition(test_dict2, 'lengthMoreThan', 1) == False
        assert pass_condition(test_dict2, 'lengthEqual', 1)
        assert pass_condition(test_dict3, 'lengthLessThan', 1) == False
        assert pass_condition(test_dict3, 'lengthMoreThan', 1)
        assert pass_condition(test_dict3, 'lengthEqual', 1) == False

        assert pass_condition(test_dict1, 'withKey', 'a') == False
        assert pass_condition(test_dict2, 'withKey', 'a')
        assert pass_condition(test_dict1, 'withoutKey', 'a')
        assert pass_condition(test_dict2, 'withoutKey', 'a') == False

        assert pass_condition(test_list1, 'containAtLeastOneOf', test_list1) == False
        assert pass_condition(test_list1, 'containAtLeastOneOf', test_list2) == False
        assert pass_condition(test_list2, 'containAtLeastOneOf', test_list2)
        assert pass_condition(test_list2, 'containAtLeastOneOf', ['b']) == False
        assert pass_condition(test_list3, 'containAtLeastOneOf', ['c']) == False
        assert pass_condition(test_list3, 'containAtLeastOneOf', ['c', 'b'])
        assert pass_condition('', 'containAtLeastOneOf', test_list1) == False
        assert pass_condition('a', 'containAtLeastOneOf', test_list2)
        assert pass_condition(test_list2, 'containAtLeastOneOf', '') == False
        assert pass_condition(test_list2, 'containAtLeastOneOf', 'a')
        assert pass_condition(test_list1, 'containAtLeastOneDifferentFrom', test_list1) == False
        assert pass_condition(test_list1, 'containAtLeastOneDifferentFrom', test_list3) == False
        assert pass_condition(test_list2, 'containAtLeastOneDifferentFrom', test_list1)
        assert pass_condition(test_list2, 'containAtLeastOneDifferentFrom', test_list2) == False
        assert pass_condition(test_list2, 'containAtLeastOneDifferentFrom', test_list3) == False
        assert pass_condition(['c'], 'containAtLeastOneDifferentFrom', test_list3)
        assert pass_condition(test_list3, 'containAtLeastOneDifferentFrom', test_list3) == False
        assert pass_condition(test_list3, 'containAtLeastOneDifferentFrom', test_list2)
        assert pass_condition(test_list3, 'containAtLeastOneDifferentFrom', test_list1)
        assert pass_condition('', 'containAtLeastOneDifferentFrom', test_list1) == False
        assert pass_condition('a', 'containAtLeastOneDifferentFrom', test_list3) == False
        assert pass_condition('d', 'containAtLeastOneDifferentFrom', test_list3)
        assert pass_condition(test_list1, 'containAtLeastOneDifferentFrom', 'a') == False
        assert pass_condition(test_list2, 'containAtLeastOneDifferentFrom', 'd')
        assert pass_condition(test_list1, 'containNoneOf', test_list1)
        assert pass_condition(test_list2, 'containNoneOf', test_list2) == False
        assert pass_condition(test_list1, 'containNoneOf', 'a')
        assert pass_condition('a', 'containNoneOf', test_list1)

        assert pass_condition('abcdefg', 'match', '.*cde.*')
        assert pass_condition('abcdefg', 'notMatch', '.*cde.*') == False
        assert pass_condition('abcdefg', 'match', '.*345.*') == False
        assert pass_condition('abcdefg', 'notMatch', '.*345.*')
        assert pass_condition('abcdefg', 'notMatch', '.*345.*')
        assert pass_condition('abcdefg', 'match', ['.*xyx.*', '.*pqr.*']) == False
        assert pass_condition('abcdefg', 'match', ['.*xyx.*', '.*345.*', '.*cde.*'])

        date1 = '2016-04-11 12:20:26.996000+00:00'
        date2 = '2017-04-11 12:20:26.996000+00:00'
        date3 = datetime.datetime.now() - datetime.timedelta(days=1)
        date4 = datetime.datetime.now() - datetime.timedelta(days=100)
        date5 = datetime.datetime.now() - datetime.timedelta(hours=5)
        assert pass_condition(date1, 'priorToDate', date2)
        assert pass_condition(date2, 'priorToDate', date1) == False
        assert pass_condition(date3, 'olderThan', [90, 'days']) == False
        assert pass_condition(date4, 'olderThan', [90, 'days'])
        assert pass_condition(date5, 'olderThan', [90, 'minutes'])
        assert pass_condition(date5, 'olderThan', [360, 'minutes']) == False
        assert pass_condition(date5, 'olderThan', [1, 'hours'])
        assert pass_condition(date5, 'olderThan', [6, 'hours']) == False
        try:
            assert pass_condition(date5, 'olderThan', [6, 'unittest']) == False
        except Exception:
            pass

        try:
            assert pass_condition(date5, 'olderThan', '90') == False
        except Exception:
            pass

        assert pass_condition(date3, 'newerThan', [90, 'days'])
        assert pass_condition(date4, 'newerThan', [90, 'days']) == False
        assert pass_condition(date4, 'newerThan', ['90', 'days']) == False

        assert pass_condition('192.168.0.1', 'inSubnets', '192.168.0.0/24')
        assert pass_condition('192.168.0.1', 'inSubnets', ['192.168.0.0/24'])
        assert pass_condition('192.168.1.1', 'inSubnets', ['192.168.0.0/24']) == False
        assert pass_condition('192.168.1.1', 'notInSubnets', ['192.168.0.0/24'])

        src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        src_file = os.path.join(src_dir, 'policy1.json')

        with open(src_file) as f:
            testpolicy = json.load(f)
        assert pass_condition(testpolicy['Statement'][0], 'containAction', 'iam:GetUser')
        assert pass_condition(testpolicy['Statement'][0], 'containAction', 'iam:CreateUser') == False
        assert pass_condition(testpolicy['Statement'][1], 'containAction', 'iam:CreateUser')
        assert pass_condition(testpolicy['Statement'][2], 'containAction', 'iam:CreateUser')
        assert pass_condition(testpolicy['Statement'][0], 'notContainAction', 'iam:CreateUser')
        assert pass_condition(testpolicy['Statement'][0], 'notContainAction', 'iam:GetUser') == False
        assert pass_condition(testpolicy['Statement'][0], 'containAtLeastOneAction', '') == False
        assert pass_condition(testpolicy['Statement'][0], 'containAtLeastOneAction', 'iam:GetUser')
        assert pass_condition(testpolicy['Statement'][0], 'containAtLeastOneAction', ['iam:CreateUser', 'iam:GetUser'])

        src_file = os.path.join(src_dir, 'statement1.json')
        with open(src_file) as f:
            stringstatement = f.read()
        assert pass_condition(stringstatement, 'containAction', 'iam:GetUser')
        assert pass_condition(stringstatement, 'containAtLeastOneAction', 'iam:GetUser')

        assert pass_condition('123456789012', 'isSameAccount', '123456789012')
        assert pass_condition(['123456789013', '123456789012'], 'isSameAccount', '123456789012')
        assert pass_condition('arn:aws:iam::123456789012:root', 'isSameAccount', '123456789012')
        assert pass_condition('arn:aws:iam::123456789012:user/name', 'isSameAccount', '123456789012')
        assert pass_condition('arn:aws:iam::123456789012:role/name', 'isSameAccount', '123456789012')
        assert pass_condition('123456789012', 'isSameAccount', '123456789013') == False
        assert pass_condition('arn:aws:iam::123456789012:root', 'isSameAccount', '123456789013') == False
        assert pass_condition('123456789012', 'isCrossAccount', '123456789013')
        assert pass_condition(['123456789013', '123456789012'], 'isCrossAccount', '123456789013')
        assert pass_condition('arn:aws:iam::123456789012:root', 'isCrossAccount', '123456789013')
        assert pass_condition({'AWS': 'arn:aws:iam::123456789012:root'}, 'isCrossAccount', '123456789013')
        assert pass_condition(
            [{'AWS': 'arn:aws:iam::123456789013:root'}, {'AWS': 'arn:aws:iam::123456789012:root'}],
            'isCrossAccount',
            '123456789013'
        )

        assert pass_condition(["a", "b", "arn:aws:iam::111111111111:role/*"], "containAtLeastOneMatching", ".*[*].*")
        assert pass_condition(["*"], "containAtLeastOneMatching", ".*[*].*")
        assert not pass_condition(["a", "b"], "containAtLeastOneMatching", ".*[*].*")
        assert not pass_condition([], "containAtLeastOneMatching", ".*[*].*")

        try:
            pass_condition('foo', 'bar', 'baz')
        except Exception:
            pass

        return
