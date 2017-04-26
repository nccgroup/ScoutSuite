#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

try:
    from opinel.utils.globals import check_requirements
    from opinel.utils.console import configPrintException, printInfo
except Exception as e:
    print('Error: Scout2 depends on the opinel package. Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

from AWSScout2 import AWSCONFIG
from AWSScout2.cli_parser import ListallArgumentParser
from AWSScout2.output.console import format_listall_output, generate_listall_output
from AWSScout2.output.html import Scout2Report
from AWSScout2.rules.ruleset import Ruleset
from AWSScout2.rules.utils import recurse


########################################
##### Main
########################################

def main():

    # Parse arguments
    parser = ListallArgumentParser()
    args = parser.parse_args()

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    if not check_requirements(os.path.realpath(__file__)):
        return 42

    # Support multiple environments
    for profile_name in args.profile:

        # Load the config
        report = Scout2Report(profile_name, args.report_dir, args.timestamp)
        aws_config = report.jsrw.load_from_file(AWSCONFIG)
        services = aws_config['service_list']

        # Create a ruleset with only whatever rules were specified...
        if args.config:
            ruleset = Ruleset(filename = 'sample', load_rules = False)
            ruleset.ruleset['rules'][0]['filename'] = args.config
            ruleset.init_rules(services, args.ip_ranges, '', False) # aws_config['aws_account_id, False)
            # Need to set the arguments values args.config_args
        else:
            # TODO:
            #args = args
            #config = {}
            #config['conditions'] = args.conditions if hasattr(args, 'conditions') else []
            #config['mapping'] = args.mapping if hasattr(args, 'mapping') else []
            pass

        # Get single rule... TODO: clean
        tmp = ruleset.rules.pop(ruleset.rules.keys()[0])
        rule = tmp.pop(tmp.keys()[0])

        # Set the keys to output
        if len(args.keys):
            # 1. Explicitly provided on the CLI
            rule['keys'] = args.keys
        elif len(args.keys_file):
            # 2. Explicitly provided files that contain the list of keys
            rule['keys'] = []
            for filename in args.keys_file:
                with open(filename, 'rt') as f:
                    rule['keys'] += json.load(f)['keys']
        else:
            try:
                # 3. Load default set of keys based on path
                target_path = config['display_path'] if 'display_path' in config else config['path']
                with open('listall-configs/%s.json' % target_path) as f:
                    rule['keys'] = json.load(f)['keys']
            except:
                # 4. Print the object name
                rule['keys'] = ['name']

        # Recursion
        if len(args.path):
            rule['path'] = args.path[0]
        target_path = rule['path'].split('.')
        current_path = []
        resources = recurse(aws_config['services'], aws_config['services'], target_path, current_path, rule)

        # Prepare the output format
        (lines, template) = format_listall_output(args.format_file, 'foo', args.format, rule)

        # Print the output
        printInfo(generate_listall_output(lines, resources, aws_config, template, []))


#
# Load rule from a JSON config file
#
def load_config_from_json(rule_metadata, ip_ranges, aws_account_id, rule_type = 'rules'):
    config = None
    config_file = rule_metadata['filename']
    if not config_file.startswith('rules/') and not config_file.startswith('filters/'):
        config_file = '%s/%s' % (rule_type, config_file)
    config_args = rule_metadata['args'] if 'args' in rule_metadata else []
    try:
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
