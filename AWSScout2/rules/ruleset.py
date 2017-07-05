# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
import json
import os
import re
import shutil

from opinel.utils.console import printDebug, printError, printException, printInfo
from opinel.utils.fs import read_ip_ranges
from opinel.utils.globals import manage_dictionary

from AWSScout2.rules import condition_operators
from AWSScout2.rules.rule_definition import RuleDefinition
from AWSScout2.rules.rule import Rule
from AWSScout2.rules.utils import recurse

finding_levels = ['danger', 'warning']

# First search local under ./rules and ./rulesets
# Then search from package files
# Then error


re_ip_ranges_from_file = re.compile(r'_IP_RANGES_FROM_FILE_\((.*?),\s*(.*?)\)')
re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')
re_list_value = re.compile(r'_LIST_\((.*?)\)')
aws_ip_ranges_filename = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'

FILTERS_DIR = 'filters'
FINDINGS_DIR = 'findings'
RULESETS_DIR = 'rulesets'
DEFAULT_RULESET = '%s/default.json' % RULESETS_DIR


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
            self.prepare_rules()

        # This should be moved into its own call from Scout2....
        #aws_account_id = ''
        #self.init_rules(services, ip_ranges, aws_account_id, False)


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


    def prepare_rules(self, attributes = []):
        """
        Update the ruleset's rules by duplicating fields as required by the HTML ruleset generator

        :return:
        """
        for filename in self.rule_definitions:
            if filename in self.rules:
                for rule in self.rules[filename]:
                    rule.set_definition(self.rule_definitions, attributes)

        # TODO : this is missing handling of the ip ranges and AWS account ID


    def update_ruleset(self, rules_dir):
        if rules_dir == None:
            return
        self.available_rules = {}
        parameterized_rules = []
        self.services = []
        for rule in self.ruleset['rules']:
            rule['filename'] = rule['filename'].replace('rules/', '')
            if not 'args' in rule:
                self.available_rules[rule['filename']] = rule
            else:
                parameterized_rules.append(rule)
        # Add default location
        rules_dir.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/findings'))
        for dir in rules_dir:
            rule_filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
            for rule_filename in rule_filenames:
                self.services.append(rule_filename.split('-')[0].lower())
                printDebug('Loading %s' % rule_filename)
                with open('%s/%s' % (dir, rule_filename), 'rt') as f:
                    rule = json.load(f)
                    if not 'key' in rule and not 'arg_names' in rule:
                        # Non-parameterized rule, save it
                        if rule_filename in self.available_rules:
                            self.available_rules[rule_filename].update(rule)
                        else:
                            self.available_rules[rule_filename] = rule
                            self.available_rules[rule_filename]['enabled'] = False
                            if 'level' not in self.available_rules[rule_filename]:
                                self.available_rules[rule_filename]['level'] = 'danger'
                                self.available_rules[rule_filename]['filename'] = rule_filename
                    else:
                        # Parameterized rules, find all occurences and save N times
                        parameterized_rule_found = False
                        for prule in parameterized_rules:
                            if prule['filename'] == rule_filename:
                                parameterized_rule_found = True
                                for k in rule:
                                    prule[k] = self.set_argument_values(rule[k], prule['args'],
                                                                   convert=True) if k != 'conditions' else rule[k]
                                key = prule.pop('key') if 'key' in prule else prule['filename']
                                args = prule.pop('args')
                                if not 'arg_names' in prule:
                                    printError('No arg names key in %s' % rule_filename)
                                    continue
                                arg_names = prule.pop('arg_names')
                                if len(args) != len(arg_names):
                                    printError('Error: rule %s expects %d arguments but was provided %d.' % (
                                    rule_filename, len(arg_names), len(args)))
                                    continue
                                prule['args'] = []
                                for (arg_name, arg_value) in zip(arg_names, args):
                                    prule['args'].append({'arg_name': arg_name, 'arg_value': arg_value})
                                if 'level' not in prule:
                                    prule['level'] = 'danger'
                                    self.available_rules[key] = prule
                        if not parameterized_rule_found:
                            # Save once with no parameters
                            self.available_rules[rule_filename] = rule
                            self.available_rules[rule_filename]['enabled'] = False
                            if 'level' not in self.available_rules[rule_filename]:
                                self.available_rules[rule_filename]['level'] = 'danger'
                                self.available_rules[rule_filename]['filename'] = rule_filename
                            args = []
                            for a in rule['arg_names']:
                                args.append({'arg_name': a, 'arg_value': ''})
                                self.available_rules[rule_filename]['args'] = args
                            printDebug('Saving rule without parameter value: %s' % rule_filename)


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
        ruleset_found = False
        if environment_name != 'default':
            for f in os.listdir(os.getcwd()):
                if fnmatch.fnmatch(f, '*.' + environment_name + '.json'):
                    ruleset_found = True
            if ruleset_found and prompt_4_yes_no("A ruleset whose name matches your environment name was found in %s. Would you like to use it instead of the default one" % f):
                self.filename = f
        if not ruleset_found:
            self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/rulesets/default.json')





    #
    # Load rule from a JSON config file
    #
    def load_json_rule(self, rule_metadata, ip_ranges, aws_account_id):
        config = None
        config_file = rule_metadata['filename']
        config_args = rule_metadata['args'] if 'args' in rule_metadata else []
        # Determine the file path
        if not os.path.isfile(config_file):
            # Not a valid relative / absolute path, check locally under findings/ or filters/
            if not config_file.startswith('findings/') and not config_file.startswith('filters/'):
                config_file = '%s/%s' % (self.rule_type, config_file)
            if not os.path.isfile(config_file):
                config_file = os.path.join(self.rules_data_path, config_file)
        # Read the file
        try:
            #print('Reading %s' % config_file)
            with open(config_file, 'rt') as f:
                config = f.read()
            # Replace arguments
            for idx, argument in enumerate(config_args):
                config = config.replace('_ARG_'+str(idx)+'_', str(argument).strip())
            config = json.loads(config)
            config['filename'] = rule_metadata['filename']
            if 'args' in rule_metadata:
                config['args'] = rule_metadata['args']
            # Load lists from files
            for c1 in config['conditions']:
                if c1 in condition_operators:
                    continue
                if not type(c1[2]) == list and not type(c1[2]) == dict:
                    values = re_ip_ranges_from_file.match(c1[2])
                    if values:
                        filename = values.groups()[0]
                        conditions = json.loads(values.groups()[1])
                        if filename == aws_ip_ranges_filename:
                             c1[2] = read_ip_ranges(aws_ip_ranges_filename, False, conditions, True)
                        elif filename == ip_ranges_from_args:
                            c1[2] = []
                            for ip_range in ip_ranges:
                                c1[2] = c1[2] + read_ip_ranges(ip_range, True, conditions, True)
                    if c1[2] and aws_account_id:
                        if not type(c1[2]) == list:
                            c1[2] = c1[2].replace('_AWS_ACCOUNT_ID_', aws_account_id)
    
                    # Set lists
                    list_value = re_list_value.match(str(c1[2]))
                    if list_value:
                        values = []
                        for v in list_value.groups()[0].split(','):
                            values.append(v.strip())
                        c1[2] = values
        except Exception as e:
            printException(e)
            printError('Error: failed to read the rule from %s' % config_file)
        return config


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

