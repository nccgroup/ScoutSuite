# -*- coding: utf-8 -*-

import os

from opinel.utils.console import configPrintException, printDebug

from AWSScout2.rules.rule import Rule
from AWSScout2.rules.ruleset import Ruleset

class TestAWSScout2RulesRuleset:

    def setup(self):
        configPrintException(True)
        self.test_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_ruleset_001 = os.path.join(self.test_dir, 'data/test-ruleset.json')
        self.test_ruleset_002 = os.path.join(self.test_dir, 'data/test-ruleset-absolute-path.json')


    def test_ruleset_class(self):
        test001 = Ruleset(filename = self.test_ruleset_001)
        assert('iam-password-policy-no-expiration.json' in test001.rules)
        assert(type(test001.rules['iam-password-policy-no-expiration.json']) == list)
        assert(type(test001.rules['iam-password-policy-no-expiration.json'][0] == Rule))
        assert(hasattr(test001.rules['iam-password-policy-no-expiration.json'][0], 'path'))
        for rule in test001.rules:
            printDebug(test001.rules[rule][0].to_string())
        test002 = Ruleset(filename = self.test_ruleset_002)
        for rule in test002.rules:
            printDebug(test002.rules[rule][0].to_string())
        test003 = Ruleset(filename = 'tests/data/no-such-file.json')
        assert(test003.rules == [])
        test004 = Ruleset(filename = 'tests/data/invalid-file.json')
        test005 = Ruleset(filename = self.test_ruleset_001, ruleset_generator = True)


    def test_find_file(self):
        test101 = Ruleset().find_file(self.test_ruleset_001)
        test102 = Ruleset().find_file('default')


    def test_search_ruleset(self):
        test201 = Ruleset().search_ruleset('test', no_prompt = True)

