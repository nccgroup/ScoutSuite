#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from opinel.utils.console import configPrintException, printInfo
    from opinel.utils.credentials import read_creds
    from opinel.utils.globals import check_requirements
except Exception as e:
    print('Error: Scout2 depends on the opinel package. Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

from AWSScout2 import AWSCONFIG, __version__ as scout2_version
from AWSScout2.cli_parser import Scout2ArgumentParser
from AWSScout2.configs.scout2 import  Scout2Config
from AWSScout2.output.html import Scout2Report
from AWSScout2.rules.exceptions import process_exceptions
from AWSScout2.rules.ruleset import Ruleset
from AWSScout2.rules.preprocessing import preprocessing
from AWSScout2.rules.postprocessing import postprocessing


########################################
##### Main
########################################

def main():

    # Parse arguments
    parser = Scout2ArgumentParser()
    args = parser.parse_args()

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    if not check_requirements(os.path.realpath(__file__)):
        return 42

    # Set the profile name
    profile_name = args.profile[0]

    # Search for AWS credentials
    if not args.fetch_local:
        credentials = read_creds(args.profile[0], args.csv_credentials, args.mfa_serial, args.mfa_code)
        if credentials['AccessKeyId'] is None:
            return 42

    # Create a new Scout2 config
    report = Scout2Report(profile_name, args.report_dir, args.timestamp)
    aws_config = Scout2Config(profile_name, args.report_dir, args.timestamp, args.services, args.skipped_services)

    if not args.fetch_local:

        # Fetch data from AWS APIs if not running a local analysis
        try:
            aws_config.fetch(credentials, regions=args.regions, partition_name=args.partition_name)
        except KeyboardInterrupt:
            printInfo('\nCancelled by user')
            return 130
        aws_config = report.jsrw.to_dict(aws_config)

    else:

        # Reload to flatten everything into a python dictionary
        aws_config = report.jsrw.load_from_file(AWSCONFIG)

    # Pre processing
    preprocessing(aws_config, args.ip_ranges, args.ip_ranges_name_key)

    # Analyze config
    ruleset = Ruleset(profile_name, filename = args.ruleset, ip_ranges = args.ip_ranges)
    ruleset.analyze(aws_config)

    # Create display filters
    filters = Ruleset(filename = 'filters.json', rule_type = 'filters')
    filters.analyze(aws_config)

    # Handle exceptions
    process_exceptions(aws_config, args.exceptions[0])

    # Finalize
    postprocessing(aws_config, report.current_time, ruleset)

    # Save config and create HTML report
    report.save(aws_config, {}, args.force_write, args.debug)
