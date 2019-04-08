#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import copy
from concurrent.futures import ThreadPoolExecutor
import os
import webbrowser

from ScoutSuite.output.report_file import ReportFile
from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser
from ScoutSuite.core.console import set_config_debug_level, print_info, print_debug, print_error
from ScoutSuite.core.exceptions import RuleExceptions
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.core.ruleset import Ruleset
from ScoutSuite.core.server import Server
from ScoutSuite.output.html import ScoutSuiteReport
from ScoutSuite.output.utils import get_filename
from ScoutSuite.providers import get_provider
from ScoutSuite.providers.base.authentication_strategy_factory import get_authentication_strategy


def main(args=None):
    """
    Main method that runs a scan
    """

    if not args:
        parser = ScoutSuiteArgumentParser()
        args = parser.parse_args()

    # Get the dictionnary to get None instead of a crash
    args = args.__dict__

    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=args.get('max_workers')))
    loop.run_until_complete(run_scan(args))
    loop.close()

# noinspection PyBroadException
async def run_scan(args):

    # Configure the debug level
    set_config_debug_level(args.get('debug'))

    print_info('Launching Scout')

    print_info('Authenticating to cloud provider')
    auth_strategy = get_authentication_strategy(args.get('provider'))
    credentials = auth_strategy.authenticate(profile=args.get('profile'),
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

    if not credentials:
        return 401

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
                                  result_format=args.get('result_format'),
                                  credentials=credentials)


    report_file_name = generate_report_name(cloud_provider.provider_code, args)

    if args.get('database_name'):
        report_name = args.get('database_name') if isinstance(args.get('database_name'), str) else report_file_name
        database_file, _ = get_filename(ReportFile.results, report_name, args.get('report_dir'), extension="db")
        Server.init(database_file, args.get('host_ip'), args.get('host_port'))
        return

    # TODO: move this to after authentication, so that the report can be more specific to what's being scanned.
    # For example if scanning with a GCP service account, the SA email can only be known after authenticating...
    # Create a new report
    report = ScoutSuiteReport(args.get('provider'), report_file_name, args.get('report_dir'), args.get('timestamp'),
                              result_format=args.get('result_format'))

    # Complete run, including pulling data from provider
    if not args.get('fetch_local'):

        # Fetch data from provider APIs
        try:
            print_info('Gathering data from APIs')
            await cloud_provider.fetch(regions=args.get('regions'))
        except KeyboardInterrupt:
            print_info('\nCancelled by user')
            return 130

        # Update means we reload the whole config and overwrite part of it
        if args.get('update'):
            print_info('Updating existing data')
            current_run_services = copy.deepcopy(cloud_provider.services)
            last_run_dict = report.encoder.load_from_file(ReportFile.results)
            cloud_provider.services = last_run_dict['services']
            for service in cloud_provider.service_list:
                cloud_provider.services[service] = current_run_services[service]

    # Partial run, using pre-pulled data
    else:
        print_info('Using local data')
        # Reload to flatten everything into a python dictionary
        last_run_dict = report.encoder.load_from_file(ReportFile.results)
        for key in last_run_dict:
            setattr(cloud_provider, key, last_run_dict[key])

    # Pre processing
    cloud_provider.preprocessing(
        args.get('ip_ranges'), args.get('ip_ranges_name_key'))

    # Analyze config
    print_info('Running rule engine')
    finding_rules = Ruleset(environment_name=args.get('profile'),
                            cloud_provider=args.get('provider'),
                            filename=args.get('ruleset'),
                            ip_ranges=args.get('ip_ranges'),
                            aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(finding_rules)
    processing_engine.run(cloud_provider)

    # Create display filters
    print_info('Applying display filters')
    filter_rules = Ruleset(cloud_provider=args.get('provider'),
                           filename='filters.json',
                           rule_type='filters',
                           aws_account_id=cloud_provider.aws_account_id)
    processing_engine = ProcessingEngine(filter_rules)
    processing_engine.run(cloud_provider)

    if args.get('exceptions')[0]:
        print_info('Applying exceptions')
        try:
            exceptions = RuleExceptions(
                args.get('profile'), args.get('exceptions')[0])
            exceptions.process(cloud_provider)
            exceptions = exceptions.exceptions
        except Exception as e:
            print_debug(
                'Failed to load exceptions. The file may not exist or may have an invalid format.')
            exceptions = {}
    else:
        exceptions = {}
    # Handle exceptions
    try:
        exceptions = RuleExceptions(
            args.get('profile'), args.get('exceptions')[0])
        exceptions.process(cloud_provider)
        exceptions = exceptions.exceptions
    except Exception as e:
        print_debug(
            'Warning, failed to load exceptions. The file may not exist or may have an invalid format.')
        exceptions = {}

    # Finalize
    cloud_provider.postprocessing(report.current_time, finding_rules)

    # Save config and create HTML report
    html_report_path = report.save(cloud_provider, exceptions, args.get('force_write'),
                                   args.get('debug'))

    # Open the report by default
    if not args.get('no_browser'):
        print_info('Opening the HTML report')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0


def generate_report_name(provider_code, args):
    # TODO this should be done within the providers
    # A pre-requisite to this is to generate report AFTER authentication
    if provider_code == 'aws':
        if args.get('profile'):
            report_file_name = 'aws-%s' % args.get('profile')
        else:
            report_file_name = 'aws'
    elif provider_code == 'gcp':
        if args.get('project_id'):
            report_file_name = 'gcp-%s' % args.get('project_id')
        elif args.get('organization_id'):
            report_file_name = 'gcp-%s' % args.get('organization_id')
        elif args.get('folder_id'):
            report_file_name = 'gcp-%s' % args.get('folder_id')
        else:
            report_file_name = 'gcp'
    elif provider_code == 'azure':
        report_file_name = 'azure'
    else:
        report_file_name = 'unknown'
    return report_file_name
