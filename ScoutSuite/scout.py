import asyncio
import copy
import os
import webbrowser

from concurrent.futures import ThreadPoolExecutor

from ScoutSuite.output.report_file import ReportFile
from ScoutSuite.core.console import set_config_debug_level, print_info, print_exception
from ScoutSuite.core.exceptions import RuleExceptions
from ScoutSuite.core.processingengine import ProcessingEngine
from ScoutSuite.core.ruleset import Ruleset
from ScoutSuite.core.server import Server
from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser
from ScoutSuite.output.html import ScoutReport
from ScoutSuite.output.utils import get_filename
from ScoutSuite.providers import get_provider
from ScoutSuite.providers.base.authentication_strategy_factory import get_authentication_strategy


def run(provider,
        profile,
        user_account, service_account,
        cli, msi, service_principal, file_auth, tenant_id, subscription_id,
        client_id, client_secret,
        username, password,
        project_id, folder_id, organization_id, all_projects,
        report_name, report_dir,
        timestamp,
        services, skipped_services,
        thread_config,  # TODO deprecate
        result_format,
        database_name, host_ip, host_port,
        max_workers,
        regions,
        fetch_local, update,
        ip_ranges, ip_ranges_name_key,
        ruleset, exceptions,
        force_write,
        debug,
        no_browser):
    """
    Run a scout job in an async event loop.
    """

    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=max_workers))
    loop.run_until_complete(_run(**locals()))  # pass through all the parameters
    loop.close()


async def _run(provider,
               profile,
               user_account, service_account,
               cli, msi, service_principal, file_auth, tenant_id, subscription_id,
               client_id, client_secret,
               username, password,
               project_id, folder_id, organization_id, all_projects,
               report_name, report_dir,
               timestamp,
               services, skipped_services,
               thread_config,  # TODO deprecate
               result_format,
               database_name, host_ip, host_port,
               regions,
               fetch_local, update,
               ip_ranges, ip_ranges_name_key,
               ruleset, exceptions,
               force_write,
               debug,
               no_browser,
               **kwargs):
    """
    Run a scout job.
    """

    # Configure the debug level
    set_config_debug_level(debug)

    print_info('Launching Scout')

    print_info('Authenticating to cloud provider')
    auth_strategy = get_authentication_strategy(provider)
    try:
        credentials = auth_strategy.authenticate(profile=profile,
                                                 user_account=user_account,
                                                 service_account=service_account,
                                                 cli=cli,
                                                 msi=msi,
                                                 service_principal=service_principal,
                                                 file_auth=file_auth,
                                                 tenant_id=tenant_id,
                                                 subscription_id=subscription_id,
                                                 client_id=client_id,
                                                 client_secret=client_secret,
                                                 username=username,
                                                 password=password)

        if not credentials:
            return 401
    except Exception as e:
        print_exception('Authentication failure: {}'.format(e))
        return 401

    # Create a cloud provider object
    cloud_provider = get_provider(provider=provider,
                                  profile=profile,
                                  project_id=project_id,
                                  folder_id=folder_id,
                                  organization_id=organization_id,
                                  all_projects=all_projects,
                                  report_dir=report_dir,
                                  timestamp=timestamp,
                                  services=services,
                                  skipped_services=skipped_services,
                                  thread_config=thread_config,
                                  credentials=credentials)

    # Create a new report
    report_name = report_name if report_name else cloud_provider.get_report_name()
    report = ScoutReport(cloud_provider.provider_code,
                         report_name,
                         report_dir,
                         timestamp,
                         result_format=result_format)

    if database_name:
        database_file, _ = get_filename(ReportFile.results, report_name, report_dir, extension="db")
        Server.init(database_file, host_ip, host_port)
        return

    # Complete run, including pulling data from provider
    if not fetch_local:

        # Fetch data from provider APIs
        try:
            print_info('Gathering data from APIs')
            await cloud_provider.fetch(regions=regions)
        except KeyboardInterrupt:
            print_info('\nCancelled by user')
            return 130

        # Update means we reload the whole config and overwrite part of it
        if update:
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
        ip_ranges, ip_ranges_name_key)

    # Analyze config
    print_info('Running rule engine')
    finding_rules = Ruleset(cloud_provider=cloud_provider.provider_code,
                            environment_name=cloud_provider.environment,
                            filename=ruleset,
                            ip_ranges=ip_ranges,
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
    if exceptions:
        print_info('Applying exceptions')
        try:
            exceptions = RuleExceptions(profile, exceptions)
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
        cloud_provider, exceptions, force_write, debug)

    # Open the report by default
    if not no_browser:
        print_info('Opening the HTML report')
        url = 'file://%s' % os.path.abspath(html_report_path)
        webbrowser.open(url, new=2)

    return 0


def main():
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    # Get the dictionary to get None instead of a crash
    args = args.__dict__

    run(args.get('provider'),
        args.get('profile'),
        args.get('user_account'), args.get('service_account'),
        args.get('cli'), args.get('msi'), args.get('service_principal'), args.get('file_auth'), args.get('tenant_id'),
        args.get('subscription_id'),
        args.get('client_id'), args.get('client_secret'),
        args.get('username'), args.get('password'),
        args.get('project_id'), args.get('folder_id'), args.get('organization_id'), args.get('all_projects'),
        args.get('report_name'), args.get('report_dir'),
        args.get('timestamp'),
        args.get('services'), args.get('skipped_services'),
        args.get('thread_config'),  # todo deprecate
        args.get('result_format'),
        args.get('database_name'),
        args.get('host_ip'),
        args.get('host_port'),
        args.get('max_workers'),
        args.get('regions'),
        args.get('fetch_local'), args.get('update'),
        args.get('ip_ranges'), args.get('ip_ranges_name_key'),
        args.get('ruleset'), args.get('exceptions'),
        args.get('force_write'),
        args.get('debug'),
        args.get('no_browser'))
