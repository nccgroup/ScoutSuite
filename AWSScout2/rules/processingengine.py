# -*- coding: utf-8 -*-

from opinel.utils.console import printDebug, printError, printException
from opinel.utils.globals import manage_dictionary

from AWSScout2.rules.utils import recurse

class ProcessingEngine(object):
    """

    """

    def __init__(self, ruleset):
        # Organize rules by path
        self.ruleset = ruleset
        self.rules = {}
        for filename in self.ruleset.rules:
            for rule in self.ruleset.rules[filename]:
                if not rule.enabled:
                    continue
                manage_dictionary(self.rules, rule.path, [])
                self.rules[rule.path].append(rule)


    def run(self, aws_config, skip_dashboard = False):
        # Clean up existing findings
        for service in aws_config['services']:
            aws_config['services'][service][self.ruleset.rule_type] = {}

        # Process each rule
        for finding_path in self.rules:
            for rule in self.rules[finding_path]:
                
                if not rule.enabled:  # or rule.service not in []: # TODO: handle this...
                    continue

                printDebug('Processing %s rule[%s]: "%s"' % (rule.service, rule.filename, rule.description))
                finding_path = rule.path
                path = finding_path.split('.')
                service = path[0]
                manage_dictionary(aws_config['services'][service], self.ruleset.rule_type, {})
                aws_config['services'][service][self.ruleset.rule_type][rule.key] = {}
                aws_config['services'][service][self.ruleset.rule_type][rule.key]['description'] = rule.description
                aws_config['services'][service][self.ruleset.rule_type][rule.key]['path'] = rule.path
                for attr in ['level', 'id_suffix', 'display_path']:
                    if hasattr(rule, attr):
                        aws_config['services'][service][self.ruleset.rule_type][rule.key][attr] = getattr(rule, attr)
                try:
                    setattr(rule, 'checked_items', 0)
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['items'] = recurse(aws_config['services'], aws_config['services'], path, [], rule, True)
                    if skip_dashboard:
                        continue
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['dashboard_name'] = rule.dashboard_name
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['checked_items'] = rule.checked_items
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['flagged_items'] = len(aws_config['services'][service][self.ruleset.rule_type][rule.key]['items'])
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['service'] = rule.service
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['rationale'] = rule.rationale if hasattr(rule, 'rationale') else 'N/A'
                except Exception as e:
                    printException(e)
                    printError('Failed to process rule defined in %s' % rule.filename)
                    # Fallback if process rule failed to ensure report creation and data dump still happen
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['checked_items'] = 0
                    aws_config['services'][service][self.ruleset.rule_type][rule.key]['flagged_items'] = 0

