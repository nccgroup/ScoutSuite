# -*- coding: utf-8 -*-

import os

from mock import patch
from opinel.utils.console import configPrintException, printDebug

from ScoutSuite.core.rule import Rule
from ScoutSuite.core.ruleset import Ruleset


class TestAWSScout2RulesRuleset:

    def setup(self):
        configPrintException(True)
        self.test_dir = os.path.dirname(os.path.realpath(__file__))

        self.test_ruleset_001 = os.path.join(self.test_dir, 'data/test-ruleset.json')
        self.test_ruleset_002 = os.path.join(self.test_dir, 'data/test-ruleset-absolute-path.json')

    def test_ruleset_class(self):
        test001 = Ruleset(filename=self.test_ruleset_001)
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
            printDebug(test001.rules[rule][0].to_string())

        assert (test_file_key in test001.rule_definitions)
        assert (test001.rule_definitions[test_file_key].description == "Password expiration disabled")
        for rule_def in test001.rule_definitions:
            printDebug(str(test001.rule_definitions[rule_def]))

        test002 = Ruleset(filename=self.test_ruleset_002)
        for rule in test002.rules:
            printDebug(test002.rules[rule][0].to_string())
        test005 = Ruleset(filename=self.test_ruleset_001, ruleset_generator=True)

    def test_ruleset_file_not_exist(self):
        test003 = Ruleset(cloud_provider='aws', filename='tests/data/no-such-file.json')
        assert (test003.rules == [])

    def test_ruleset_invalid(self):
        test004 = Ruleset(cloud_provider='aws', filename='tests/data/invalid-file.json')
        assert (test004.rules == [])

    def test_path_for_cloud_providers(self):
        target = Ruleset(filename=self.test_ruleset_001)
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/aws/rules'))

        target = Ruleset(filename=self.test_ruleset_001, cloud_provider="aws")
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/aws/rules'))

        target = Ruleset(filename=self.test_ruleset_001, cloud_provider="azure")
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/azure/rules'))

        target = Ruleset(filename=self.test_ruleset_001, cloud_provider="gcp")
        assert (os.path.samefile(target.rules_data_path, './ScoutSuite/providers/gcp/rules'))

    def test_path_for_ruletypes(self):
        rpath = "./ScoutSuite/providers/aws/rules/"

        target = Ruleset(filename='default.json')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/default.json'))
        target = Ruleset(filename='default')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/default.json'))

        target = Ruleset(filename='filters.json')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/filters.json'))
        target = Ruleset(filename='filters')
        assert (os.path.samefile(target.filename, rpath + 'rulesets/filters.json'))

    def test_path_search_default(self):
        target = Ruleset(filename=None)
        norms = os.path.normpath(os.path.join(self.test_dir, '../ScoutSuite/core/data/rulesets/default.json'))
        # assert (os.path.normpath(target.filename) == norms)

        assert (os.path.exists("ruleset-notexist.json") == False)
        target = Ruleset(filename=None, environment_name="notexist")
        norms = os.path.normpath(os.path.join(self.test_dir, '../ScoutSuite/core/data/rulesets/default.json'))
        # assert (os.path.normpath(target.filename) == norms)

    @patch("ScoutSuite.core.ruleset.prompt_4_yes_no", return_value=True)
    def test_path_search_withenv_prompt_yes(self, patched):
        with open("ruleset-special.json", "w") as f:
            f.write(".")

        target = Ruleset(filename=None, environment_name="special")
        norms = os.path.abspath('./ruleset-special.json')
        # assert (os.path.normpath(target.filename) == norms)

        os.unlink("ruleset-special.json")

    @patch("ScoutSuite.core.ruleset.prompt_4_yes_no", return_value=False)
    def test_path_search_withenv_prompt_no(self, patched):
        with open("ruleset-special.json", "w") as f:
            f.write(".")

        target = Ruleset(filename=None, environment_name="special")
        norms = os.path.normpath(os.path.join(self.test_dir, '../ScoutSuite/core/data/rulesets/default.json'))
        # assert (os.path.normpath(target.filename) == norms)

        os.unlink("ruleset-special.json")

    def test_find_file(self):
        test101 = Ruleset(cloud_provider='aws').find_file(self.test_ruleset_001)
        test102 = Ruleset(cloud_provider='aws').find_file('default')

    def test_search_ruleset(self):
        test201 = Ruleset(cloud_provider='aws').search_ruleset('test', no_prompt=True)
