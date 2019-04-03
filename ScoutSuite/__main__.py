import asyncio
import copy
from concurrent.futures import ThreadPoolExecutor
import os
import webbrowser

from ScoutSuite import DEFAULT_RESULT_FILE
from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser
from ScoutSuite.core.console import set_config_debug_level, print_info, print_exception
from ScoutSuite.core.exceptions import RuleExceptions
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.core.ruleset import Ruleset
from ScoutSuite.output.html import ScoutReport
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
    try:
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
                                                 password=args.get('password'),
                                                 access_key_id=args.get('access_key_id'),
                                                 access_key_secret=args.get('access_key_secret'),
                                                 )

        if not credentials:
            return 401
    except Exception as e:
        print_exception('Authentication failure: {}'.format(e))
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
                                  credentials=credentials)

    # Create a new report
    report_name = args.get('report_name') if args.get('report_name') else cloud_provider.get_report_name()
    report = ScoutReport(cloud_provider.provider_code,
                         report_name,
                         args.get('report_dir'),
                         args.get('timestamp'))

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
            last_run_dict = report.jsrw.load_from_file('RESULTS')
            cloud_provider.services = last_run_dict['services']
            for service in cloud_provider.service_list:
                cloud_provider.services[service] = current_run_services[service]

    # Partial run, using pre-pulled data
    else:
        print_info('Using local data')
        # Reload to flatten everything into a python dictionary
        last_run_dict = report.jsrw.load_from_file('RESULTS')
        for key in last_run_dict:
            setattr(cloud_provider, key, last_run_dict[key])

    # Pre processing
    cloud_provider.preprocessing(
        args.get('ip_ranges'), args.get('ip_ranges_name_key'))

    # Analyze config
    print_info('Running rule engine')
    finding_rules = Ruleset(cloud_provider=cloud_provider.provider_code,
                            environment_name=cloud_provider.environment,
                            filename=args.get('ruleset'),
                            ip_ranges=args.get('ip_ranges'),
                            account_id=cloud_provider.account_id)
    processing_engine = ProcessingEngine(finding_rules)
    processing_engine.run(cloud_provider)

    # Create display filters
    print_info('Applying display filters')
    filter_rules = Ruleset(cloud_provider=cloud_provider.provider_code,
                           environment_name=cloud_provider.environment,
                           rule_type='filters',
                           account_id=cloud_provider.account_id)
    processing_engine = ProcessingEngine(filter_rules)
    processing_engine.run(cloud_provider)

    # Handle exceptions
    if args.get('exceptions'):
        print_info('Applying exceptions')
        try:
            exceptions = RuleExceptions(
                args.get('profile'), args.get('exceptions'))
            exceptions.process(cloud_provider)
            exceptions = exceptions.exceptions
        except Exception as e:
            print_exception('Failed to load exceptions: {}'.format(e))
            exceptions = {}
    else:
        exceptions = {}

    # Finalize
    cloud_provider.postprocessing(report.current_time, finding_rules)

    # Save config and create HTML report
    html_report_path = report.save(
        cloud_provider, exceptions, args.get('force_write'), args.get('debug'))

    # Open the report by default
    if not args.get('no_browser'):
        print_info('Opening the HTML report')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0
