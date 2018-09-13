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

from ScoutSuite import AWSCONFIG
from ScoutSuite.cli_parser import ScoutSuiteArgumentParser
# from ScoutSuite.configs.scout2 import Scout2Config
from ScoutSuite.output.html import Scout2Report
from ScoutSuite.core.exceptions import RuleExceptions
from ScoutSuite.core.ruleset import Ruleset
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.providers import get_provider


def main():
    """
    Main method that runs a scan

    :return:
    """

    # Parse arguments
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    # Configure the debug level
    configPrintException(args.debug)

    # Create a cloud provider object
    cloud_provider = get_provider(provider=args.provider,
                                  profile=args.profile[0],
                                  project_id=args.project_id,
                                  organization_id=args.organization_id,
                                  report_dir=args.report_dir,
                                  timestamp=args.timestamp,
                                  services=args.services,
                                  skipped_services=args.skipped_services,
                                  thread_config=args.thread_config)

    # Create a new report
    report = Scout2Report(args.profile[0], args.report_dir, args.timestamp)

    # Complete run, including pulling data from provider
    if not args.fetch_local:
        # Authenticate to the cloud provider
        authenticated = cloud_provider.authenticate(profile=args.profile[0],
                                                    csv_credentials=args.csv_credentials,
                                                    mfa_serial=args.mfa_serial,
                                                    mfa_code=args.mfa_code,
                                                    key_file=args.key_file,
                                                    user_account=args.user_account,
                                                    service_account=args.service_account)
        if not authenticated:
            return 42

        # Fetch data from provider APIs
        try:
            cloud_provider.fetch(regions=args.regions)
        except KeyboardInterrupt:
            printInfo('\nCancelled by user')
            return 130

        # Update means we reload the whole config and overwrite part of it
        # TODO this is currently broken - unsure if will be supporterd in the future
        # if args.update:
        #     new_aws_config = copy.deepcopy(aws_config)
        #     aws_config = report.jsrw.load_from_file(AWSCONFIG)
        #     for service in new_aws_config['service_list']:
        #         # Per service only for now, may add per region & per VPC later...
        #         aws_config['services'][service] = new_aws_config['services'][service]
        #     # Update the metadata too
        #     aws_config['metadata'] = Scout2Config('default', None, None, [], []).metadata

    # Partial run, using pre-pulled data
    else:
        # Reload to flatten everything into a python dictionary
        # TODO this is currently broken - unsure if will be supporterd in the future
        # aws_config = report.jsrw.load_from_file(AWSCONFIG)
        pass

    # Pre processing
    cloud_provider.preprocessing(args.ip_ranges, args.ip_ranges_name_key)

    # # Analyze config
    finding_rules = Ruleset(environment_name=args.profile[0],
                            cloud_provider=args.provider,
                            filename=args.ruleset,
                            ip_ranges=args.ip_ranges,
                            aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(finding_rules)
    processing_engine.run(cloud_provider)

    # Create display filters
    filter_rules = Ruleset(cloud_provider=args.provider,
                           filename='filters.json',
                           rule_type='filters',
                           aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(filter_rules)
    processing_engine.run(cloud_provider)

    # Handle exceptions
    try:
        exceptions = RuleExceptions(args.profile[0], args.exceptions[0])
        exceptions.process(cloud_provider)
        exceptions = exceptions.exceptions
    except Exception as e:
        printDebug('Warning, failed to load exceptions. The file may not exist or may have an invalid format.')
        exceptions = {}

    # Finalize
    cloud_provider.postprocessing(report.current_time, finding_rules)

    # Get organization data if it exists
    # TODO this is AWS-specific
    # try:
    #     profile = AWSProfiles.get(args.profile[0])[0]
    #     if 'source_profile' in profile.attributes:
    #         organization_info_file = os.path.join(
    #             os.path.expanduser('~/.aws/recipes/%s/organization.json' % profile.attributes['source_profile']))
    #         if os.path.isfile(organization_info_file):
    #             with open(organization_info_file, 'rt') as f:
    #                 org = {}
    #                 accounts = json.load(f)
    #                 for account in accounts:
    #                     account_id = account.pop('Id')
    #                     org[account_id] = account
    #                 aws_config['organization'] = org
    # except Exception as e:
    #     pass

    # Save config and create HTML report
    html_report_path = report.save(cloud_provider, exceptions, args.force_write, args.debug)

    # Open the report by default
    if not args.no_browser:
        printInfo('Opening the HTML report...')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0
