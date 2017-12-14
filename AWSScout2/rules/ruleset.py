# -*- coding: utf-8 -*-

import fnmatch
import json
import os
import shutil
import tempfile

from opinel.utils.console import printDebug, printError, printException, printInfo, prompt_4_yes_no

from AWSScout2.rules.rule_definition import RuleDefinition
from AWSScout2.rules.rule import Rule

aws_ip_ranges_filename = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'



class Ruleset(object):
    """
    TODO

    :ivar rules:                        List of rules defined in the ruleset
    :ivar rule_definitions:             Definition of all rules found
    :ivar ??
    """

    def __init__(self, environment_name = 'default', filename = None, name = None, rules_dir = [], rule_type = 'findings', ip_ranges = [], aws_account_id = None, ruleset_generator = False):
        self.rules_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        self.environment_name = environment_name
        self.rule_type = rule_type
        # Ruleset filename
        self.filename = self.find_file(filename)
        if not self.filename:
            self.search_ruleset(environment_name)
        printDebug('Loading ruleset %s' % self.filename)
        self.name = os.path.basename(self.filename).replace('.json','') if not name else name
        self.load(self.rule_type)
        self.shared_init(ruleset_generator, rules_dir, aws_account_id, ip_ranges)


    def to_string(self):
        return (str(vars(self)))


    def shared_init(self, ruleset_generator, rule_dirs, aws_account_id, ip_ranges):

        # Load rule definitions
        if not hasattr(self, 'rule_definitions'):
            self.load_rule_definitions(ruleset_generator, rule_dirs)

        # Prepare the rules
        params = {}
        params['aws_account_id'] = aws_account_id
        if ruleset_generator:
            self.prepare_rules(attributes =  ['description', 'key', 'rationale'], params = params)
        else:
            self.prepare_rules(ip_ranges = ip_ranges, params = params)


    def load(self, rule_type, quiet = False):
        """
        Open a JSON file definiting a ruleset and load it into a Ruleset object

        :param quiet:
        :return:
        """
        if self.filename and os.path.exists(self.filename):
            try:
                with open(self.filename, 'rt') as f:
                    ruleset = json.load(f)
                    self.about = ruleset['about'] if 'about' in ruleset else ''
                    self.rules = {}
                    for filename in ruleset['rules']:
                        self.rules[filename] = []
                        for rule in ruleset['rules'][filename]:
                            self.handle_rule_versions(filename, rule_type, rule)
            except Exception as e:
                printException(e)
                printError('Error: ruleset file %s contains malformed JSON.' % self.filename)
                self.rules = []
                self.about = ''
        else:
            self.rules = []
            if not quiet:
                printError('Error: the file %s does not exist.' % self.filename)


    def load_rules(self, file, rule_type, quiet = False):
        file.seek(0)
        ruleset = json.load(file)
        self.about = ruleset['about']
        self.rules = {}
        for filename in ruleset['rules']:
            self.rules[filename] = []
            for rule in ruleset['rules'][filename]:
                self.handle_rule_versions(filename, rule_type, rule)


    def handle_rule_versions(self, filename, rule_type, rule):
        """
        For each version of a rule found in the ruleset, append a new Rule object
        """
        if 'versions' in rule:
            versions = rule.pop('versions')
            for version_key_suffix in versions:
                version = versions[version_key_suffix]
                version['key_suffix'] = version_key_suffix
                tmp_rule = dict(rule, **version)
                self.rules[filename].append(Rule(filename, rule_type, tmp_rule))
        else:
            self.rules[filename].append(Rule(filename, rule_type, rule))


    def prepare_rules(self, attributes = [], ip_ranges = [], params = {}):
        """
        Update the ruleset's rules by duplicating fields as required by the HTML ruleset generator

        :return:
        """
        for filename in self.rule_definitions:
            if filename in self.rules:
                for rule in self.rules[filename]:
                    rule.set_definition(self.rule_definitions, attributes, ip_ranges, params)
            else:
                self.rules[filename] = []
                new_rule = Rule(filename, self.rule_type, {'enabled': False, 'level': 'danger'})
                new_rule.set_definition(self.rule_definitions, attributes, ip_ranges, params)
                self.rules[filename].append(new_rule)


    def load_rule_definitions(self, ruleset_generator = False, rule_dirs = []):
        """
        Load definition of rules declared in the ruleset

        :param services:
        :param ip_ranges:
        :param aws_account_id:
        :param generator:
        :return:
        """

        # Load rules from JSON files
        self.rule_definitions = {}
        for rule_filename in self.rules:
            for rule in self.rules[rule_filename]:
                if not rule.enabled and not ruleset_generator:
                    continue
            self.rule_definitions[os.path.basename(rule_filename)] = RuleDefinition(rule_filename, rule_dirs = rule_dirs)
        # In case of the ruleset generator, list all available built-in rules
        if ruleset_generator:
            rule_dirs.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/findings'))
            rule_filenames = []
            for rule_dir in rule_dirs:
                rule_filenames += [f for f in os.listdir(rule_dir) if os.path.isfile(os.path.join(rule_dir, f))]
            for rule_filename in rule_filenames:
                if rule_filename not in self.rule_definitions:
                    self.rule_definitions[os.path.basename(rule_filename)] = RuleDefinition(rule_filename)


    def search_ruleset(self, environment_name, no_prompt = False):
        """

        :param environment_name:
        :return:
        """
        ruleset_found = False
        if environment_name != 'default':
            ruleset_file_name = 'ruleset-%s.json' % environment_name
            ruleset_file_path = os.path.join(os.getcwd(), ruleset_file_name)
            if os.path.exists(ruleset_file_path):
                if no_prompt or prompt_4_yes_no("A ruleset whose name matches your environment name was found in %s. Would you like to use it instead of the default one" % ruleset_file_name):
                    ruleset_found = True
                    self.filename = ruleset_file_path
        if not ruleset_found:
            self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/rulesets/default.json')


    def find_file(self, filename, filetype = 'rulesets'):
        """

        :param filename:
        :param filetype:
        :return:
        """
        if filename and not os.path.isfile(filename):
            # Not a valid relative / absolute path, check Scout2's data under findings/ or filters/
            if not filename.startswith('findings/') and not filename.startswith('filters/'):
                filename = '%s/%s' % (filetype, filename)
            if not os.path.isfile(filename):
                filename = os.path.join(self.rules_data_path, filename)
            if not os.path.isfile(filename) and not filename.endswith('.json'):
                filename = self.find_file('%s.json' % filename, filetype)
        return filename


class TmpRuleset(Ruleset):

    def __init__(self, rule_dirs = [], rule_filename = None, rule_args = [], rule_level = 'danger'):
        self.rule_type = 'findings'
        tmp_ruleset = {'rules': {}, 'about': 'Temporary, single-rule ruleset.'}
        tmp_ruleset['rules'][rule_filename] = []
        rule = {'enabled': True, 'level': rule_level}
        if len(rule_args):
            rule['args'] = rule_args
        tmp_ruleset['rules'][rule_filename].append(rule)
        tmp_ruleset_file = tempfile.TemporaryFile('w+t')
        tmp_ruleset_file.write(json.dumps(tmp_ruleset))

        self.load_rules(file = tmp_ruleset_file, rule_type = 'findings', quiet = False)

        self.shared_init(False, rule_dirs, '', [])

