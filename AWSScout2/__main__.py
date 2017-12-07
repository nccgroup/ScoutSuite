#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import os
import sys
import webbrowser

try:
    from opinel.utils.aws import get_aws_account_id, get_partition_name
    from opinel.utils.console import configPrintException, printInfo, printDebug
    from opinel.utils.credentials import read_creds
    from opinel.utils.globals import check_requirements
    from opinel.utils.profiles import AWSProfiles
except Exception as e:
    print('Error: Scout2 depends on the opinel package. Install all the requirements with the following command:')
    print('  $ pip install -r requirements.txt')
    print(e)
    sys.exit(42)

from AWSScout2 import AWSCONFIG, __version__ as scout2_version
from AWSScout2.cli_parser import Scout2ArgumentParser
from AWSScout2.configs.scout2 import  Scout2Config
from AWSScout2.output.html import Scout2Report
from AWSScout2.rules.exceptions import RuleExceptions
from AWSScout2.rules.ruleset import Ruleset
from AWSScout2.rules.preprocessing import preprocessing
from AWSScout2.rules.postprocessing import postprocessing
from AWSScout2.rules.processingengine import ProcessingEngine


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
    aws_config = Scout2Config(profile_name, args.report_dir, args.timestamp, args.services, args.skipped_services, args.thread_config)

    if not args.fetch_local:

        # Fetch data from AWS APIs if not running a local analysis
        try:
            aws_config.fetch(credentials, regions=args.regions, partition_name = get_partition_name(credentials))
        except KeyboardInterrupt:
            printInfo('\nCancelled by user')
            return 130
        aws_config = report.jsrw.to_dict(aws_config)

        # Set the account ID
        aws_config['aws_account_id'] = get_aws_account_id(credentials)

        # Update means we reload the whole config and overwrite part of it
        if args.update == True:
            new_aws_config = copy.deepcopy(aws_config)
            aws_config = report.jsrw.load_from_file(AWSCONFIG)
            for service in new_aws_config['service_list']:
                # Per service only for now, may add per region & per VPC later...
                aws_config['services'][service] = new_aws_config['services'][service]
            # Update the metadata too
            aws_config['metadata'] = Scout2Config('default', None, None, [], []).metadata

    else:

        # Reload to flatten everything into a python dictionary
        aws_config = report.jsrw.load_from_file(AWSCONFIG)

    # Pre processing
    preprocessing(aws_config, args.ip_ranges, args.ip_ranges_name_key)

    # Analyze config
    finding_rules = Ruleset(profile_name, filename = args.ruleset, ip_ranges = args.ip_ranges, aws_account_id = aws_config['aws_account_id'])
    pe = ProcessingEngine(finding_rules)
    pe.run(aws_config)

    # Create display filters
    filter_rules = Ruleset(filename = 'filters.json', rule_type = 'filters', aws_account_id = aws_config['aws_account_id'])
    pe = ProcessingEngine(filter_rules)
    pe.run(aws_config)

    # Handle exceptions
    try:
        exceptions = RuleExceptions(profile_name, args.exceptions[0])
        exceptions.process(aws_config)
        exceptions = exceptions.exceptions
    except Exception as e:
        printDebug('Warning, failed to load exceptions. The file may not exist or may have an invalid format.')
        exceptions = {}

    # Finalize
    postprocessing(aws_config, report.current_time, finding_rules)

    # Get organization data if it exists
    try:
        profile = AWSProfiles.get(profile_name)[0]
        if 'source_profile' in profile.attributes:
            organization_info_file = os.path.join(os.path.expanduser('~/.aws/recipes/%s/organization.json' %  profile.attributes['source_profile']))
            if os.path.isfile(organization_info_file):
                with open(organization_info_file, 'rt') as f:
                    org = {}
                    accounts = json.load(f)
                    for account in accounts:
                        account_id = account.pop('Id')
                        org[account_id] = account
                    aws_config['organization'] = org
    except:
        pass

    # Save config and create HTML report
    html_report_path = report.save(aws_config, exceptions, args.force_write, args.debug)

    # Open the report by default
    if not args.no_browser:
        printInfo('Opening the HTML report...')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0
