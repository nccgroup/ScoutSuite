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
from AWSScout2.rules.rule_definition import RuleDefinition
from AWSScout2.rules.ruleset import TmpRuleset
from AWSScout2.rules.processingengine import ProcessingEngine


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
            rule_filename = args.config
            ruleset = TmpRuleset(rule_dirs = [os.getcwd()], rule_filename = args.config, rule_args = [])
        else:
            # Create a local tmp rule
            rule_dict = {'description': 'artifact'}
            rule_dict['path'] = args.path[0]
            rule_dict['conditions'] = []
            rule_filename = 'listall-artifact.json'
            with open(os.path.join(os.getcwd(), rule_filename), 'wt') as f:
                f.write(json.dumps(rule_dict))
            ruleset = TmpRuleset(rule_dirs = [os.getcwd()], rule_filename = rule_filename, rule_args = [])

        # Process the rule
        pe = ProcessingEngine(ruleset)
        pe.run(aws_config, skip_dashboard = True)

        # Retrieve items
        rule = ruleset.rules[rule_filename][0]
        rule_service = rule.service.lower()
        rule_key = rule.key
        rule_type = rule.rule_type
        resources = aws_config['services'][rule_service][rule_type][rule_key]['items']

        # Set the keys to output
        if len(args.keys):
            # 1. Explicitly provided on the CLI
            rule.keys = args.keys
        elif len(args.keys_file):
            # 2. Explicitly provided files that contain the list of keys
            rule.keys = []
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
                rule.keys = ['name']

        # Prepare the output format
        (lines, template) = format_listall_output(args.format_file, 'foo', args.format, rule)

        # Print the output
        printInfo(generate_listall_output(lines, resources, aws_config, template, []))
