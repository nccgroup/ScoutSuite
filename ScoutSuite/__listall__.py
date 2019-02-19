#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

try:
    from opinel.utils.globals import check_requirements
    from opinel.utils.console import configPrintException, printError, printException, printInfo
except Exception as e:
    print('Error: Scout2 depends on the opinel package. Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

from ScoutSuite import AWSCONFIG
from ScoutSuite.providers import get_provider
from ScoutSuite.core.ruleset import TmpRuleset
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.output.console import format_listall_output, generate_listall_output
from ScoutSuite.output.html import Scout2Report


########################################
##### Main
########################################

def main(args):
    # Configure the debug level
    configPrintException(args.debug)

    # FIXME check that all requirements are installed
    # # Check version of opinel
    # if not check_requirements(os.path.realpath(__file__)):
    #     return 42

    # Support multiple environments
    for profile_name in args.profile:

        # Load the config
        try:
            # FIXME this is specific to AWS
            report_file_name = 'aws-%s' % profile_name
            report = Scout2Report('aws', report_file_name, args.report_dir, args.timestamp)
            aws_config = report.jsrw.load_from_file(AWSCONFIG)
            services = aws_config['service_list']
        except Exception as e:
            printException(e)
            printError('Error, failed to load the configuration for profile %s' % profile_name)
            continue

        # Create a ruleset with only whatever rules were specified...
        if args.config:
            rule_filename = args.config
            ruleset = TmpRuleset(environment_name=args.profile[0],
                                 cloud_provider='aws',
                                 rule_dirs=[os.getcwd()],
                                 rule_filename=args.config,
                                 rule_args=args.config_args)
        elif len(args.path) > 0:
            # Create a local tmp rule
            rule_dict = {'description': 'artifact'}
            rule_dict['path'] = args.path[0]
            rule_dict['conditions'] = []
            rule_filename = 'listall-artifact.json'
            with open(os.path.join(os.getcwd(), rule_filename), 'wt') as f:
                f.write(json.dumps(rule_dict))
            ruleset = TmpRuleset(rule_dirs=[os.getcwd()], rule_filename=rule_filename, rule_args=[])
        else:
            printError(
                'Error, you must provide either a rule configuration file or the path to the resources targeted.')
            continue

        # FIXME is broken in Scout Suite, only handles AWS
        cloud_provider = get_provider(provider='aws',
                                      profile=args.profile[0])

        # Process the rule
        pe = ProcessingEngine(ruleset)
        pe.run(cloud_provider, skip_dashboard=True)

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
                    rule.keys += json.load(f)['keys']
        else:
            try:
                # 3. Load default set of keys based on path
                target_path = rule.display_path if hasattr(rule, 'display_path') else rule.path
                listall_configs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                   'output/data/listall-configs')
                target_file = os.path.join(listall_configs_dir, '%s.json' % target_path)
                if os.path.isfile(target_file):
                    with open(target_file, 'rt') as f:
                        rule.keys = json.load(f)['keys']
            except:
                # 4. Print the object name
                rule.keys = ['name']

        # Prepare the output format
        (lines, template) = format_listall_output(args.format_file[0], None, args.format, rule)

        # Print the output
        printInfo(generate_listall_output(lines, resources, aws_config, template, []))
