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
        assert (printError.call_count == 1)  # is this expected ??
        assert ("test-ruleset-absolute-path.json does not exist." in printError.call_args_list[0][0][0])

        # ruleset_generator=True should auto-discover every built-in findings
        # rule, not just the ones explicitly listed in the ruleset file (see
        # Ruleset.load_rule_definitions's `if ruleset_generator:` branch).
        test005 = Ruleset(cloud_provider='aws', filename=self.test_ruleset_001, ruleset_generator=True)
        findings_dir = os.path.join(test005.rules_data_path, 'findings')
        findings_count = len([f for f in os.listdir(findings_dir) if os.path.isfile(os.path.join(findings_dir, f))])
        assert (len(test005.rule_definitions) == findings_count)
        assert ('acm-certificate-with-close-expiration-date.json' in test005.rule_definitions)
        assert (hasattr(test005.rules[test_file_key][0], 'description'))

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
        # An existing absolute/relative path is returned unchanged (the
        # `if filename and not os.path.isfile(filename):` guard short-circuits).
        test101 = Ruleset(cloud_provider='aws').find_file(self.test_ruleset_001)
        assert (test101 == self.test_ruleset_001)

        # A bare ruleset name with no path/extension resolves to
        # <rules_data_path>/rulesets/<name>.json, same as the filename=
        # constructor argument tested in test_path_for_ruletypes.
        test102 = Ruleset(cloud_provider='aws').find_file('default')
        rpath = "./ScoutSuite/providers/aws/rules/"
        assert (os.path.samefile(test102, rpath + 'rulesets/default.json'))

    def test_search_ruleset(self):
        target = Ruleset(cloud_provider='aws')
        # search_ruleset mutates target.filename in place and has no return value.
        test201 = target.search_ruleset('test', no_prompt=True)
        assert (test201 is None)
        # No ruleset-test.json exists under rulesets/, so it must fall back to default.json.
        assert (os.path.samefile(target.filename, os.path.join(target.rules_data_path, 'rulesets/default.json')))
