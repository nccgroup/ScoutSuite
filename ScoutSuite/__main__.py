#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import os
import webbrowser

from opinel.utils.console import configPrintException, printInfo, printDebug
from opinel.utils.profiles import AWSProfiles

from ScoutSuite.cli_parser import ScoutSuiteArgumentParser
from ScoutSuite import AWSCONFIG
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
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    # Get the dictionnary to get None instead of a crash
    args = args.__dict__

    # Configure the debug level
    configPrintException(args.get('debug'))

    # Create a cloud provider object
    cloud_provider = get_provider(provider=args.get('provider'),
                                  profile=args.get('profile'),
                                  project_id=args.get('project_id'),
                                  folder_id=args.get('folder_id'),
                                  organization_id=args.get('organization_id'),
                                  all_projects=args.get('all_projects'),
                                  report_dir=args.get('report_dir'),
                                  timestamp=args.get('timestamp'),
                                  services=args.get('services'),
                                  skipped_services=args.get('skipped_services'),
                                  thread_config=args.get('thread_config'),
                                  )

    report_file_name = generate_report_name(cloud_provider.provider_code, args)

    # TODO move this to after authentication, so that the report can be more specific to what's being scanned.
    # For example if scanning with a GCP service account, the SA email can only be known after authenticating...
    # Create a new report
    report = Scout2Report(args.get('provider'), report_file_name, args.get('report_dir'), args.get('timestamp'))

    # Complete run, including pulling data from provider
    if not args.get('fetch_local'):
        # Authenticate to the cloud provider
        authenticated = cloud_provider.authenticate(profile=args.get('profile'),
                                                    csv_credentials=args.get('csv_credentials'),
                                                    mfa_serial=args.get('mfa_serial'),
                                                    mfa_code=args.get('mfa_code'),
                                                    user_account=args.get('user_account'),
                                                    service_account=args.get('service_account'),
                                                    cli=args.get('cli'),
                                                    msi=args.get('msi'),
                                                    service_principal=args.get('service_principal'),
                                                    file_auth=args.get('file_auth'),
                                                    tenant_id=args.get('tenant_id'),
                                                    subscription_id=args.get('subscription_id'),
                                                    client_id=args.get('client_id'),
                                                    client_secret=args.get('client_secret'),
                                                    username=args.get('username'),
                                                    password=args.get('password')
                                                    )

        if not authenticated:
            return 42

        # Fetch data from provider APIs
        try:
            cloud_provider.fetch(regions=args.get('regions'))
        except KeyboardInterrupt:
            printInfo('\nCancelled by user')
            return 130

        # Update means we reload the whole config and overwrite part of it
        if args.get('update'):
            current_run_services = copy.deepcopy(cloud_provider.services)
            last_run_dict = report.jsrw.load_from_file(AWSCONFIG)
            cloud_provider.services = last_run_dict['services']
            for service in cloud_provider.service_list:
                cloud_provider.services[service] = current_run_services[service]

    # Partial run, using pre-pulled data
    else:
        # Reload to flatten everything into a python dictionary
        last_run_dict = report.jsrw.load_from_file(AWSCONFIG)
        for key in last_run_dict:
            setattr(cloud_provider, key, last_run_dict[key])

    # Pre processing
    cloud_provider.preprocessing(args.get('ip_ranges'), args.get('ip_ranges_name_key'))

    # Analyze config
    finding_rules = Ruleset(environment_name=args.get('profile'),
                            cloud_provider=args.get('provider'),
                            filename=args.get('ruleset'),
                            ip_ranges=args.get('ip_ranges'),
                            aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(finding_rules)
    processing_engine.run(cloud_provider)

    # Create display filters
    filter_rules = Ruleset(cloud_provider=args.get('provider'),
                           filename='filters.json',
                           rule_type='filters',
                           aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(filter_rules)
    processing_engine.run(cloud_provider)

    # Handle exceptions
    try:
        exceptions = RuleExceptions(args.get('profile'), args.get('exceptions')[0])
        exceptions.process(cloud_provider)
        exceptions = exceptions.exceptions
    except Exception as e:
        printDebug('Warning, failed to load exceptions. The file may not exist or may have an invalid format.')
        exceptions = {}

    # Finalize
    cloud_provider.postprocessing(report.current_time, finding_rules)

    # TODO this is AWS-specific - move to postprocessing?
    # Get organization data if it exists
    try:
        profile = AWSProfiles.get(args.get('profile'))[0]
        if 'source_profile' in profile.attributes:
            organization_info_file = os.path.join(os.path.expanduser('~/.aws/recipes/%s/organization.json' %
                                                                     profile.attributes['source_profile']))
            if os.path.isfile(organization_info_file):
                with open(organization_info_file, 'rt') as f:
                    org = {}
                    accounts = json.load(f)
                    for account in accounts:
                        account_id = account.pop('Id')
                        org[account_id] = account
                    setattr(cloud_provider, 'organization', org)
    except Exception as e:
        pass

    # Save config and create HTML report
    html_report_path = report.save(cloud_provider, exceptions, args.get('force_write'), args.get('debug'))

    # Open the report by default
    if not args.get('no_browser'):
        printInfo('Opening the HTML report...')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0


def generate_report_name(provider_code, args):
    if provider_code == 'aws':
        if args.get('profile'):
            report_file_name = 'aws-%s' % args.get('profile')[0]
        else:
            report_file_name = 'aws'
    if provider_code == 'gcp':
        if args.get('project_id'):
            report_file_name = 'gcp-%s' % args.get('project_id')
        elif args.get('organization_id'):
            report_file_name = 'gcp-%s' % args.get('organization_id')
        elif args.get('folder_id'):
            report_file_name = 'gcp-%s' % args.get('folder_id')
        else:
            report_file_name = 'gcp'
    if provider_code == 'azure':
        report_file_name = 'azure'
    return report_file_name
