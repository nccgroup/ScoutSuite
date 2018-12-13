# -*- coding: utf-8 -*-

import os

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
        test003 = Ruleset(filename='tests/data/no-such-file.json')
        assert (test003.rules == [])

    def test_ruleset_invalid(self):
        test004 = Ruleset(filename='tests/data/invalid-file.json')
        assert (test004.rules == [])

    def test_find_file(self):
        test101 = Ruleset(cloud_provider='aws').find_file(self.test_ruleset_001)
        test102 = Ruleset(cloud_provider='aws').find_file('default')

    def test_search_ruleset(self):
        test201 = Ruleset(cloud_provider='aws').search_ruleset('test', no_prompt=True)
