import os

from unittest import mock
import unittest
from ScoutSuite.core.console import set_logger_configuration, print_debug
from ScoutSuite.core.rule import Rule
from ScoutSuite.core.ruleset import Ruleset


class TestScoutRulesRuleset(unittest.TestCase):

    def setUp(self):
        set_logger_configuration(is_debug=True)
        self.test_dir = os.path.dirname(os.path.realpath(__file__))

        self.test_ruleset_001 = os.path.join(self.test_dir, 'data/test-ruleset.json')
        self.test_ruleset_002 = os.path.join(self.test_dir, 'data/test-ruleset-absolute-path.json')

    @mock.patch("ScoutSuite.core.ruleset.print_error")
    def test_ruleset_class(self, printError):
        test001 = Ruleset(cloud_provider='aws', filename=self.test_ruleset_001)
        assert (os.path.isdir(test001.rules_data_path))
        assert (os.path.isfile(test001.filename))
        assert (test001.name == "test-ruleset")
        assert (test001.about == "regression test")

        test_file_key = 'iam-password-policy-no-expiration.json'
        assert (test_file_key in test001.rules)
        assert (type(test001.rules[test_file_key]) == list)
        assert (type(test001.rules[test_file_key][0] == Rule))
        assert (hasattr(test001.rules[test_file_key][0], 'path'))
        for rule in test001.rules:
            print_debug(test001.rules[rule][0].to_string())

        assert (test_file_key in test001.rule_definitions)
        assert (test001.rule_definitions[test_file_key].description == "Password Expiration Disabled")
        for rule_def in test001.rule_definitions:
            print_debug(str(test001.rule_definitions[rule_def]))
        assert (printError.call_count == 0)

        test002 = Ruleset(cloud_provider='aws', filename=self.test_ruleset_002)
        for rule in test002.rules:
            print_debug(test002.rules[rule][0].to_string())
        assert (printError.call_count == 1) # is this expected ??
        assert ("test-ruleset-absolute-path.json does not exist." in printError.call_args_list[0][0][0])

        test005 = Ruleset(cloud_provider='aws', filename=self.test_ruleset_001, ruleset_generator=True)

    @mock.patch("ScoutSuite.core.ruleset.print_error")
    def test_ruleset_file_not_exist(self, printError):
        test003 = Ruleset(cloud_provider='aws', filename='tests/data/no-such-file.json')
        assert (test003.rules == [])
        assert (printError.call_count == 1)
        assert ("no-such-file.json does not exist" in printError.call_args_list[0][0][0])

    @mock.patch("ScoutSuite.core.ruleset.print_exception")
    def test_ruleset_invalid(self, printException):
        test004 = Ruleset(cloud_provider='aws', filename='tests/data/invalid-file.json')
        assert (test004.rules == [])
        assert (printException.call_count == 1)
        assert ("invalid-file.json contains malformed JSON" in printException.call_args_list[0][0][0])

    def test_path_for_cloud_providers(self):
        target = Ruleset(cloud_provider='aws', filename=self.test_ruleset_001)
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/aws/rules'))

        target = Ruleset(cloud_provider='azure', filename=self.test_ruleset_001)
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/azure/rules'))

        target = Ruleset(cloud_provider='gcp', filename=self.test_ruleset_001)
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/gcp/rules'))

    def test_path_for_ruletypes(self):
        rpath = "./ScoutSuite/providers/aws/rules/"

        target = Ruleset(cloud_provider='aws', filename='default.json')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/default.json'))
        target = Ruleset(cloud_provider='aws', filename='default')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/default.json'))

        target = Ruleset(cloud_provider='aws', filename='filters.json')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/filters.json'))

        target = Ruleset(cloud_provider='aws', filename='filters')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/filters.json'))

    @mock.patch("ScoutSuite.core.ruleset.prompt_yes_no")
    def test_file_search(self, prompt_yes_no):
        prompt_yes_no.return_value = False

        target = Ruleset(cloud_provider='aws', filename=None)
        assert (prompt_yes_no.call_count == 0)
        assert (os.path.samefile(target.filename, os.path.join(target.rules_data_path, './rulesets/default.json')))

        target = Ruleset(cloud_provider='aws', environment_name="notexist", filename=None)
        assert (prompt_yes_no.call_count == 0)
        assert (os.path.samefile(target.filename, os.path.join(target.rules_data_path, './rulesets/default.json')))

        prompt_yes_no.reset_mock()
        prompt_yes_no.return_value = True

    def test_find_file(self):
        test101 = Ruleset(cloud_provider='aws').find_file(self.test_ruleset_001)
        test102 = Ruleset(cloud_provider='aws').find_file('default')

    def test_search_ruleset(self):
        test201 = Ruleset(cloud_provider='aws').search_ruleset('test', no_prompt=True)
