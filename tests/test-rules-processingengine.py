# -*- coding: utf-8 -*-

import json
import os

from opinel.utils.console import configPrintException, printError

from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.core.ruleset import Ruleset


class DummyObject(object):
    pass

class TestAWSScout2RulesProcessingEngine:

    def setup(self):
        configPrintException(True)

        # Build a fake ruleset

    #    filename = 'foobar.json'
    #    ruleset = {'rules': {}}
    #    ruleset['rules'][filename] = []
    #    ruleset['rules'][filename].append({'enabled': True, 'level': 'danger'})
    #    pass

    # finding_rules = Ruleset(profile_name, filename=args.ruleset, ip_ranges=args.ip_ranges)
    # pe = ProcessingEngine(finding_rules)
    # pe.run(aws_config)

    # TODO
    # Check that one testcase per finding rule exists (should be within default
    # reulset)

    def test_all_finding_rules(self):
        test_dir = os.path.dirname(os.path.realpath(__file__))
        test_ruleset_file_name = os.path.join(test_dir, 'data/ruleset-test.json')
        #FIXME this is only for AWS
        with open(os.path.join(test_dir, '../ScoutSuite/providers/aws/rules/rulesets/default.json'), 'rt') as f:
            ruleset = json.load(f)

        rule_counters = {'found': 0, 'tested': 0, 'verified': 0}
        for file_name in ruleset['rules']:
            rule_counters['found'] += 1
            test_config_file_name = os.path.join(test_dir, 'data/rule-configs/%s' % file_name)
            if not os.path.isfile(test_config_file_name):
                continue
            rule_counters['tested'] += 1
            test_ruleset = {'rules': {}, 'about': 'regression test'}
            test_ruleset['rules'][file_name] = []
            rule = ruleset['rules'][file_name][0]
            rule['enabled'] = True
            test_ruleset['rules'][file_name].append(rule)
            with open(test_ruleset_file_name, 'wt') as f:
                f.write(json.dumps(test_ruleset, indent=4))
            #            printError('Ruleset ::')
            #            printError(str(test_ruleset))
            rules = Ruleset(filename=test_ruleset_file_name)
            pe = ProcessingEngine(rules)
            with open(test_config_file_name, 'rt') as f:
                dummy_provider = DummyObject()
                test_config_dict = json.load(f)
                for key in test_config_dict:
                    setattr(dummy_provider, key, test_config_dict[key])
            service = file_name.split('-')[0]
            dummy_provider.service_list = [service]
            pe.run(dummy_provider)
            findings = dummy_provider.services[service]['findings']
            findings = findings[list(findings.keys())[0]]['items']
            test_result_file_name = os.path.join(test_dir, 'data/rule-results/%s' % file_name)
            if not os.path.isfile(test_result_file_name):
                printError('Expected findings:: ')
                printError(json.dumps(findings, indent=4))
                continue
            rule_counters['verified'] += 1
            with open(test_result_file_name, 'rt') as f:
                items = json.load(f)
            try:
                assert (set(sorted(findings)) == set(sorted(items)))
            except Exception as e:
                printError('Expected items:\n %s' % json.dumps(sorted(items)))
                printError('Reported items:\n %s' % json.dumps(sorted(findings)))
                assert (False)
        print('Existing  rules: %d' % rule_counters['found'])
        print('Processed rules: %d' % rule_counters['tested'])
        print('Verified  rules: %d' % rule_counters['verified'])
