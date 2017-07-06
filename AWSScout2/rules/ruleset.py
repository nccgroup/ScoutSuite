# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
import json
import os
import shutil

from opinel.utils.console import printDebug, printError, printException, printInfo

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

    def __init__(self, environment_name = 'default', filename = None, name = None, services = [], rule_type = 'findings', rules_dir = None, ip_ranges = [], ruleset_generator = False):
        self.rules_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        self.environment_name = environment_name
        self.rule_type = rule_type
        # Ruleset filename
        self.filename = self.find_file(filename)
        if not self.filename:
            self.search_ruleset(environment_name)
        self.name = os.path.basename(self.filename).replace('.json','') if not name else name

        # Load ruleset
        self.load(self.rule_type)

        # Load rule definitions
        self.load_rule_definitions(ruleset_generator)

        # Prepare the rules
        if ruleset_generator:
            self.prepare_rules(attributes =  ['description', 'key', 'rationale'])
        else:
            # aws_account_id = '' ... # TODO
            self.prepare_rules(ip_ranges = ip_ranges, params = {})


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
                    self.about = ruleset['about']
                    self.rules = {}
                    for filename in ruleset['rules']:
                        self.rules[filename] = []
                        for rule in ruleset['rules'][filename]:
                            self.rules[filename].append(Rule(filename, rule_type, rule['enabled'], rule['level'] if 'level' in rule else '', rule['args'] if 'args' in rule else []))
            except Exception as e:
                printException(e)
                printError('Error: ruleset file %s contains malformed JSON.' % self.filename)
                self.rules = []
                self.about = ''
        else:
            self.rules = []
            if not quiet:
                printError('Error: the file %s does not exist.' % self.filename)


    def prepare_rules(self, attributes = [], ip_ranges = [], params = []):
        """
        Update the ruleset's rules by duplicating fields as required by the HTML ruleset generator

        :return:
        """
        for filename in self.rule_definitions:
            if filename in self.rules:
                for rule in self.rules[filename]:
                    rule.set_definition(self.rule_definitions, attributes, ip_ranges, params)


    def html_generator(self, output_dir, metadata, force_write, debug):
        """

        :param output_dir:
        :param metadata:
        :param force_write:
        :param debug:
        :return:
        """
        # Prepare the output directories
        prepare_html_output_dir(output_dir)
        # Create the JS include file
        printInfo('Preparing the HTML ruleset generator...')
        js_ruleset = {}
        js_ruleset['name'] = self.name
        js_ruleset['available_rules'] = self.available_rules
        js_ruleset['services'] = list(sorted(set(self.services)))
        js_ruleset['ruleset_generator_metadata'] = metadata
        save_config_to_file(self.environment_name, js_ruleset, 'ruleset', output_dir, force_write, debug)
        # Create the HTML generator
        html_generator = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../rules/data/ruleset-generator.html')
        dst_html_generator = os.path.join(output_dir, 'ruleset-generator.html')
        shutil.copyfile(html_generator, dst_html_generator)
        return dst_html_generator


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


    def search_ruleset(self, environment_name):
        """

        :param environment_name:
        :return:
        """
        ruleset_found = False
        if environment_name != 'default':
            for f in os.listdir(os.getcwd()):
                if fnmatch.fnmatch(f, '*.' + environment_name + '.json'):
                    ruleset_found = True
            if ruleset_found and prompt_4_yes_no("A ruleset whose name matches your environment name was found in %s. Would you like to use it instead of the default one" % f):
                self.filename = f
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

