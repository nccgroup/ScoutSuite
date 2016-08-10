#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import stock packages
import json
import os
import webbrowser
import sys

# Import Scout2 tools
from AWSScout2 import __version__
from AWSScout2.findings import *

# Setup variables
(scout2_dir, tool_name) = os.path.split(__file__)
scout2_dir = os.path.abspath(scout2_dir)
scout2_rules_dir = '%s/%s' % (scout2_dir, RULES_DIR)
scout2_rulesets_dir = '%s/%s' % (scout2_dir, RULESETS_DIR)
ruleset_creator_path = '%s/ruleset-creator.html' % (scout2_dir)


########################################
##### Main
########################################

def main(args):

    # Setup variables
    available_rules = {}
    parameterized_rules = []
    services = []
    base_ruleset = args.base_ruleset[0]
    ruleset_name = args.ruleset_name[0]

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    min_opinel, max_opinel = get_opinel_requirement()
    if not check_opinel_version(min_opinel):
        return 42

    # Load base ruleset
    printInfo('Loading settings from the base ruleset (%s)...' % base_ruleset)
    ruleset = load_ruleset(base_ruleset)
    for rule in ruleset['rules']:
        rule['filename'] = rule['filename'].replace('rules/', '')
        if not 'args' in rule:
            available_rules[rule['filename']] = rule
        else:
            parameterized_rules.append(rule)

    # Load all available rules
    printInfo('Loading all available rules...')
    rules = [ f for f in os.listdir(scout2_rules_dir) if os.path.isfile(os.path.join(scout2_rules_dir, f)) ]
    for rule_filename in rules:
        services.append(rule_filename.split('-')[0].lower())
        with open('%s/%s' % (scout2_rules_dir, rule_filename), 'rt') as f:
            rule = json.load(f)
            if not 'key' in rule:
                # Non-parameterized rule, save it
                if rule_filename in available_rules:
                    available_rules[rule_filename].update(rule)
                else:
                    available_rules[rule_filename] = rule
                    available_rules[rule_filename]['enabled'] = False
            else:
                # Parameterized rules, find all occurences and save N times
                for prule in parameterized_rules:
                    if prule['filename'] == rule_filename:
                         for k in rule:
                             prule[k] = set_argument_values(rule[k], prule['args'], convert = True) if k != 'conditions' else rule[k]
                         key = prule.pop('key')
                         args = prule.pop('args')
                         if not 'arg_names' in prule:
                             printError('No arg names key in %s' % rule_filename)
                             continue
                         arg_names = prule.pop('arg_names')
                         if len(args) != len(arg_names):
                             printError('Error: rule %s expects %d arguments but was provided %d.' % (rule_filename, len(arg_names), len(args)))
                             continue
                         prule['args'] = []
                         for (arg_name, arg_value) in zip(arg_names, args):
                            prule['args'].append({'arg_name': arg_name, 'arg_value': arg_value})
                         available_rules[key] = prule

    ruleset = {}
    ruleset['name'] = ruleset_name
    ruleset['available_rules'] = available_rules
    ruleset['services'] = list(sorted(set(services)))
    printInfo('Preparing the HTML ruleset generator...')
    save_config_to_file('default', ruleset, force_write = True, debug = True, js_filename = AWSRULESET_FILE, quiet = True)

    # Open the HTML ruleset generator in a browser
    printInfo('Starting the HTML ruleset generator...')
    url = 'file://%s' % ruleset_creator_path
    webbrowser.open(url, new = 2)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

parser.add_argument('--base-ruleset',
                    dest='base_ruleset',
                    default=[ '%s/%s/default.json' % (scout2_dir, RULESETS_DIR) ],
                    nargs='+',
                    help='Load settings from an existing ruleset.')

parser.add_argument('--ruleset-name',
                    dest='ruleset_name',
                    default=None,
                    required=True,
                    help='Name of the ruleset to be generated.')


args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
