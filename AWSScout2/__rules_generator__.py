#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser

try:
    from opinel.utils.console import configPrintException, printInfo
    from opinel.utils.globals import check_requirements
except Exception as e:
    print('Error: Scout2 depends on the opinel package. Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

from AWSScout2.cli_parser import RulesArgumentParser
from AWSScout2.configs.scout2 import Scout2Config
from AWSScout2.rules.ruleset import Ruleset
from AWSScout2.output.html import RulesetGenerator


########################################
##### Main
########################################

def main():

    # Parse arguments
    parser = RulesArgumentParser()
    args = parser.parse_args()

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    if not check_requirements(os.path.realpath(__file__)):
        return 42

    # Load ruleset
    ruleset = Ruleset(filename = args.base_ruleset, name = args.ruleset_name, rules_dir = args.rules_dir, ruleset_generator = True)

    # Generate the HTML generator
    ruleset_generator = RulesetGenerator(args.ruleset_name, args.generator_dir)
    ruleset.ruleset_generator_metadata = Scout2Config('default', None, None, [], []).metadata
    ruleset_generator_path = ruleset_generator.save(ruleset, args.force_write, args.debug)

    # Open the HTML ruleset generator in a browser
    if not args.no_browser:
        printInfo('Starting the HTML ruleset generator...')
        url = 'file://%s' % os.path.abspath(ruleset_generator_path)
        webbrowser.open(url, new=2)
