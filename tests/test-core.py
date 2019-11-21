from nose.tools import *
from ScoutSuite.core.conditions import pass_condition
from ScoutSuite.core.cli_parser import  *


#
# Test methods for ScoutSuite/utils.py
#
class TestScoutCore:

    ########################################
    # conditions.py
    ########################################

    def test_pass_condition(self):
        assert (pass_condition(1, 'lessOrEqual', 2))
        assert (pass_condition(2, 'moreThan', 1))
        assert (pass_condition(2, 'moreOrEqual', 2))
        assert (pass_condition(None, 'null', 1))
        assert (not pass_condition(None, 'notNull', 1))
        assert (pass_condition(True, 'true', 1))
        assert (pass_condition('test', 'lengthLessThan', 6))
        assert (pass_condition('longtest', 'lengthMoreThan', 3))
        assert (pass_condition('test', 'lengthEqual', 4))
        assert (pass_condition('test with key', 'withoutKey', 'not'))
        assert (pass_condition(True, 'containString', True))
        assert (pass_condition(False, 'notContainString', True))
        assert (pass_condition([1, 2, 3], 'containAtLeastOneDifferentFrom', [1]))
        assert (pass_condition('test', 'notMatch', 'a'))
        assert (pass_condition('Thu Sep 24 10:36:28 BRST 2003', 'priorToDate', 'Thu Sep 25 10:36:28 BRST 2003'))
        assert (pass_condition('Thu Sep 24 10:36:28 BRST 2019', 'olderThan', [5, 'days']))
        assert (pass_condition('Thu Sep 24 10:36:28 BRST 3019', 'newerThan', [5, 'days']))
        assert (pass_condition(['aws'], 'isCrossAccount', 'iam'))
        assert (pass_condition(['aws'], 'isSameAccount', 'aws'))

    @raises(Exception)
    def test_pass_condition_exception(self):
        pass_condition(True, 'unknownTest', True)

    ########################################
    # cli_parser.py
    ########################################

    def test_argument_parser(self):
       test_arguments = ScoutSuiteArgumentParser()
       assert (test_arguments.parser._subparsers.title == 'The provider you want to run scout against')
       assert (test_arguments.subparsers._choices_actions[0].help == 'Run Scout against an Amazon Web Services account')
       assert (test_arguments.subparsers._choices_actions[1].help == 'Run Scout against a Google Cloud Platform account')
       assert (test_arguments.subparsers._choices_actions[2].help == 'Run Scout against a Microsoft Azure account')
       assert (test_arguments.subparsers._choices_actions[3].help == 'Run Scout against an Alibaba Cloud account')
       assert (test_arguments.subparsers._choices_actions[4].help == 'Run Scout against an Oracle Cloud Infrastructure account')