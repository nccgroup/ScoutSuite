from nose.tools import *
from ScoutSuite.core.conditions import pass_condition
from ScoutSuite.core.cli_parser import *
from ScoutSuite.core.console import prompt, prompt_overwrite, prompt_value

#
# Test methods for ScoutSuite/core
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

    ########################################
    # console.py
    ########################################

    def test_prompt(self):
        assert (prompt('test') == 'test')
        assert (prompt(['test']) == 'test')

    def test_prompt_overwrite(self):
        assert (prompt_overwrite('', True, None))
        assert (not prompt_overwrite('data/resources/dummy_resources.json', False, 'n'))
        assert (prompt_overwrite('data/resources/dummy_resources.json', False, 'y'))
        assert (prompt_overwrite('data/resources/dummy_resources.json', False, 'wrong') is None)

    def test_prompt_value(self):
        assert (prompt_value(question='', max_laps=1, test_input='test', is_question=True, choices=['test']) is None)
        assert (prompt_value(question='', max_laps=1, test_input='test', is_question=True, choices=['test'], no_confirm=True) == 'test')