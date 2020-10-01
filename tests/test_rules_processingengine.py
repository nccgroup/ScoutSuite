import json
import os
import tempfile
import unittest

from ScoutSuite.core.console import set_logger_configuration, print_error
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.core.ruleset import Ruleset


class DummyObject(object):
    pass


class TestScoutRulesProcessingEngine(unittest.TestCase):

    def setUp(self):
        set_logger_configuration(is_debug=True)
        self.rule_counters = {'found': 0, 'tested': 0, 'verified': 0}
        self.test_dir = os.path.dirname(os.path.realpath(__file__))

    # TODO
    # Check that one testcase per finding rule exists (should be within default ruleset)

    def test_all_finding_rules(self):
        ruleset_file_name = os.path.join(self.test_dir, 'data/ruleset-test.json')
        # FIXME this is only for AWS
        with open(os.path.join(self.test_dir, '../ScoutSuite/providers/aws/rules/rulesets/default.json'), 'rt') as f:
            ruleset = json.load(f)

        for rule_file_name in ruleset['rules']:
            self.rule_counters['found'] += 1
            rule = ruleset['rules'][rule_file_name][0]
            rule['enabled'] = True
            print(rule_file_name)
            self._test_rule(ruleset_file_name, rule_file_name, rule)

        print('Existing  rules: %d' % self.rule_counters['found'])
        print('Processed rules: %d' % self.rule_counters['tested'])
        print('Verified  rules: %d' % self.rule_counters['verified'])


    def _test_rule(self, ruleset_file_name, rule_file_name, rule):
        test_config_file_name = os.path.join(self.test_dir, 'data/rule-configs/%s' % rule_file_name)
        if not os.path.isfile(test_config_file_name):
            return
        self.rule_counters['tested'] += 1

        ruleset = self._generate_ruleset(rule_file_name, rule)
        pe = ProcessingEngine(ruleset)

        dummy_provider = DummyObject()
        with open(test_config_file_name, 'rt') as f:
            test_config_dict = json.load(f)
            for key in test_config_dict:
                setattr(dummy_provider, key, test_config_dict[key])
        service = rule_file_name.split('-')[0]
        dummy_provider.service_list = [service]
        pe.run(dummy_provider)
        findings = dummy_provider.services[service]['findings']
        findings = findings[list(findings.keys())[0]]['items']

        test_result_file_name = os.path.join(self.test_dir, 'data/rule-results/%s' % rule_file_name)
        if not os.path.isfile(test_result_file_name):
            print_error('Expected findings:: ')
            print_error(json.dumps(findings, indent=4))
            return

        self.rule_counters['verified'] += 1
        with open(test_result_file_name, 'rt') as f:
            items = json.load(f)

        try:
            assert (set(sorted(findings)) == set(sorted(items)))
        except Exception:
            print_error('Expected items:\n %s' % json.dumps(sorted(items)))
            print_error('Reported items:\n %s' % json.dumps(sorted(findings)))
            assert (False)

    def _generate_ruleset(self, rule_file_name, rule):
        test_ruleset = {'rules': {}, 'about': 'regression test'}
        test_ruleset['rules'][rule_file_name] = [rule]

        with tempfile.NamedTemporaryFile('wt', delete=False) as f:
            f.write(json.dumps(test_ruleset, indent=4))

        return Ruleset(cloud_provider='aws', filename=f.name)
