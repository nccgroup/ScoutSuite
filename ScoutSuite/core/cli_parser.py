import argparse
from ScoutSuite import __version__


class ScoutSuiteArgumentParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        # People will still be able to use the old --provider syntax
        self.parser.add_argument("--provider",
                                 action='store_true',
                                 dest='sinkhole',
                                 help=argparse.SUPPRESS)

        self.parser.add_argument('-v', '--version',
                                 action='version',
                                 version='Scout Suite {}'.format(__version__))

        self.common_providers_args_parser = argparse.ArgumentParser(add_help=False)

        self.subparsers = self.parser.add_subparsers(title="The provider you want to run scout against",
                                                     dest="provider")

        self._init_common_args_parser()

        self._init_aws_parser()
        self._init_gcp_parser()
        self._init_azure_parser()
        self._init_aliyun_parser()
        self._init_oci_parser()

    def _init_aws_parser(self):
        parser = self.subparsers.add_parser("aws",
                                            parents=[self.common_providers_args_parser],
                                            help="Run Scout against an Amazon Web Services account")

        aws_parser = parser.add_argument_group('Authentication modes')
        aws_auth_params = parser.add_argument_group('Authentication parameters')

        aws_auth_modes = aws_parser.add_mutually_exclusive_group(required=False)

        aws_auth_modes.add_argument('-p',
                                    '--profile',
                                    dest='profile',
                                    default=None,
                                    help='Run with a named profile')

        aws_auth_modes.add_argument('--access-keys',
                                    action='store_true',
                                    dest='aws_access_keys',
                                    help='Run with access keys')
        aws_auth_params.add_argument('--access-key-id',
                                     action='store',
                                     default=None,
                                     dest='aws_access_key_id',
                                     help='AWS Access Key ID')
        aws_auth_params.add_argument('--secret-access-key',
                                     action='store',
                                     default=None,
                                     dest='aws_secret_access_key',
                                     help='AWS Secret Access Key')
        aws_auth_params.add_argument('--session-token',
                                     action='store',
                                     default=None,
                                     dest='aws_session_token',
                                     help='AWS Session Token')

        aws_additional_parser = parser.add_argument_group('Additional arguments')

        aws_additional_parser.add_argument('-r',
                                           '--regions',
                                           dest='regions',
                                           default=[],
                                           nargs='+',
                                           help='Name of regions to run the tool in, defaults to all')
        aws_additional_parser.add_argument('-xr',
                                           '--exclude-regions',
                                           dest='excluded_regions',
                                           default=[],
                                           nargs='+',
                                           help='Name of regions to excluded from execution')
        aws_additional_parser.add_argument('--ip-ranges',
                                           dest='ip_ranges',
                                           default=[],
                                           nargs='+',
                                           help='Config file(s) that contain your known IP ranges')
        aws_additional_parser.add_argument('--ip-ranges-name-key',
                                           dest='ip_ranges_name_key',
                                           default='name',
                                           help='Name of the key containing the display name of a known CIDR')

    def _init_gcp_parser(self):
        parser = self.subparsers.add_parser("gcp",
                                            parents=[self.common_providers_args_parser],
                                            help="Run Scout against a Google Cloud Platform account")

        gcp_parser = parser.add_argument_group('Authentication modes')

        gcp_auth_modes = gcp_parser.add_mutually_exclusive_group(required=True)

        gcp_auth_modes.add_argument('-u',
                                    '--user-account',
                                    action='store_true',
                                    help='Run Scout with a Google Account')

        gcp_auth_modes.add_argument('-s',
                                    '--service-account',
                                    action='store',
                                    metavar="KEY_FILE",
                                    help='Run Scout with a Google Service Account with the specified '
                                         'Google Service Account Application Credentials file')

        gcp_scope = parser.add_argument_group('Additional arguments')

        gcp_scope.add_argument('--project-id',
                               action='store',
                               help='ID of the GCP Project to scan')

        gcp_scope.add_argument('--folder-id',
                               action='store',
                               help='ID of the GCP Folder to scan')

        gcp_scope.add_argument('--organization-id',
                               action='store',
                               help='ID of the GCP Organization to scan')

        gcp_scope.add_argument('--all-projects',
                               action='store_true',
                               help='Scan all of the accessible projects')

    def _init_azure_parser(self):
        parser = self.subparsers.add_parser("azure",
                                            parents=[self.common_providers_args_parser],
                                            help="Run Scout against a Microsoft Azure account")

        azure_parser = parser.add_argument_group('Authentication modes')
        azure_auth_params = parser.add_argument_group('Authentication parameters')

        azure_auth_modes = azure_parser.add_mutually_exclusive_group(required=True)

        # az-cli authentication
        azure_auth_modes.add_argument('-c',
                                      '--cli',
                                      action='store_true',
                                      help='Run Scout using configured azure-cli credentials')

        # username/password authentication
        azure_auth_modes.add_argument('--user-account',
                                      action='store_true',
                                      help='Run Scout with user credentials')
        azure_auth_params.add_argument('-u',
                                       '--username',
                                       action='store',
                                       default=None,
                                       dest='username',
                                       help='Username of the Azure account')
        azure_auth_params.add_argument('-p',
                                       '--password',
                                       action='store',
                                       default=None,
                                       dest='password',
                                       help='Password of the Azure account')

        # username/password authentication via browser
        azure_auth_modes.add_argument('--user-account-browser',
                                      action='store_true',
                                      help='Run Scout with user credentials, authenticating through a browser (useful when MFA is enforced)')

        # Service Principal authentication
        azure_auth_modes.add_argument('-s',
                                      '--service-principal',
                                      action='store_true',
                                      help='Run Scout with an Azure Service Principal')
        azure_auth_params.add_argument('--client-id',
                                       action='store',
                                       dest='client_id',
                                       help='Client ID of the service principal')
        azure_auth_params.add_argument('--client-secret',
                                       action='store',
                                       dest='client_secret',
                                       help='Client of the service principal')
        # Service Principal credentials in an auth file
        azure_auth_modes.add_argument('--file-auth',
                                      action='store',
                                      type=argparse.FileType('rb'),
                                      dest='file_auth',
                                      metavar="FILE",
                                      help='Run Scout with the specified credential file')

        # Managed Service Identity (MSI) authentication
        azure_auth_modes.add_argument('-m',
                                      '--msi',
                                      action='store_true',
                                      help='Run Scout with Managed Service Identity')

        # Additional arguments
        azure_scope = parser.add_argument_group('Additional arguments')

        azure_scope.add_argument('--tenant',
                                 action='store',
                                 dest='tenant_id',
                                 help='ID of the Tenant (Directory) to scan')
        azure_scope.add_argument('--subscriptions',
                                 action='store',
                                 default=[],
                                 nargs='+',
                                 dest='subscription_ids',
                                 help='IDs (separated by spaces) of the Azure subscription(s) to scan. '
                                      'By default, only the default subscription will be scanned.')
        azure_scope.add_argument('--all-subscriptions',
                                 action='store_true',
                                 dest='all_subscriptions',
                                 help='Scan all of the accessible subscriptions')

    def _init_aliyun_parser(self):
        parser = self.subparsers.add_parser("aliyun",
                                            parents=[self.common_providers_args_parser],
                                            help="Run Scout against an Alibaba Cloud account")

        aliyun_parser = parser.add_argument_group('Authentication modes')
        aliyun_auth_params = parser.add_argument_group('Authentication parameters')

        aliyun_auth_modes = aliyun_parser.add_mutually_exclusive_group(required=True)

        aliyun_auth_modes.add_argument('--access-keys',
                                       action='store_true',
                                       help='Run Scout with user credentials')

        aliyun_auth_params.add_argument('-k',
                                        '--access-key-id',
                                        action='store',
                                        default=None,
                                        dest='access_key_id',
                                        help='Access Key Id')

        aliyun_auth_params.add_argument('-s',
                                        '--access-key-secret',
                                        action='store',
                                        default=None,
                                        dest='access_key_secret',
                                        help='Access Key Secret')

    def _init_oci_parser(self):
        oci_parser = self.subparsers.add_parser("oci",
                                                parents=[self.common_providers_args_parser],
                                                help="Run Scout against an Oracle Cloud Infrastructure account")

        parser = oci_parser.add_argument_group('Authentication parameters')

        parser.add_argument('-p',
                            '--profile',
                            dest='profile',
                            default=None,
                            help='Name of the profile')


    def _init_common_args_parser(self):
        parser = self.common_providers_args_parser.add_argument_group('Scout Arguments')

        parser.add_argument('-f',
                            '--force',
                            dest='force_write',
                            default=False,
                            action='store_true',
                            help='Overwrite existing files')
        parser.add_argument('-l', '--local',
                            dest='fetch_local',
                            default=False,
                            action='store_true',
                            help='Use local data previously fetched and re-run the analysis.')
        parser.add_argument('--max-rate',
                            dest='max_rate',
                            type=int,
                            default=None,
                            help='Maximum number of API requests per second')
        parser.add_argument('--debug',
                            dest='debug',
                            default=False,
                            action='store_true',
                            help='Print the stack trace when exception occurs')
        parser.add_argument('--quiet',
                            dest='quiet',
                            default=False,
                            action='store_true',
                            help='Disables CLI output')
        parser.add_argument('--logfile',
                            dest='log_file',
                            default=None,
                            action='store',
                            nargs='?',
                            help='Additional output to the specified file')
        # parser.add_argument('--resume',
        #                     dest='resume',
        #                     default=False,
        #                     action='store_true',
        #                     help='Complete a partial (throttled) run')
        parser.add_argument('--update',
                            dest='update',
                            default=False,
                            action='store_true',
                            help='Reload all the existing data and only overwrite data in scope for this run')
        parser.add_argument('--ruleset',
                            dest='ruleset',
                            default='default.json',
                            nargs='?',
                            help='Set of rules to be used during the analysis.')
        parser.add_argument('--no-browser',
                            dest='no_browser',
                            default=False,
                            action='store_true',
                            help='Do not automatically open the report in the browser.')
        parser.add_argument('--max-workers',
                            dest='max_workers',
                            type=int,
                            default=10,
                            help='Maximum number of threads (workers) used by Scout Suite (default is 10)')
        parser.add_argument('--report-dir',
                            dest='report_dir',
                            default=None,
                            help='Path of the Scout report.')
        parser.add_argument('--report-name',
                            dest='report_name',
                            default=None,
                            help='Name of the Scout report.')
        parser.add_argument('--timestamp',
                            dest='timestamp',
                            default=False,
                            nargs='?',
                            help='Timestamp added to the name of the report (default is current time in UTC).')
        parser.add_argument('--services',
                            dest='services',
                            default=[],
                            nargs='+',
                            help='Name of in-scope services, defaults to all.')
        parser.add_argument('--list-services',
                            dest='list_services',
                            default=False,
                            action='store_true',
                            help='List available services.')
        parser.add_argument('--skip',
                            dest='skipped_services',
                            default=[],
                            nargs='+',
                            help='Name of out-of-scope services.')
        parser.add_argument('--exceptions',
                            dest='exceptions',
                            default=None,
                            nargs='?',
                            help='Exception file to use during analysis.')
        parser.add_argument('--result-format',
                            dest='result_format',
                            default='json',
                            type=str,
                            choices=['json', 'sqlite'],
                            help="[EXPERIMENTAL FEATURE] The database file format to use. JSON doesn't require a server to view the report, "
                                 "but cannot be viewed if the result file is over 400mb.")
        parser.add_argument('--serve',
                            dest="database_name",
                            default=None,
                            const=True,
                            nargs="?",
                            help="[EXPERIMENTAL FEATURE] Serve the specified result database on the server to show the report. "
                                 "This must be used when the results are exported as an sqlite database.")
        parser.add_argument('--host',
                            dest="host_ip",
                            default="127.0.0.1",
                            help="[EXPERIMENTAL FEATURE] Address on which you want the server to listen. Defaults to localhost.")
        parser.add_argument('--port',
                            dest="host_port",
                            type=int,
                            default=8000,
                            help="[EXPERIMENTAL FEATURE] Port on which you want the server to listen. Defaults to 8000.")

    def parse_args(self, args=None):
        args = self.parser.parse_args(args)

        # Cannot simply use required for backward compatibility
        if not args.provider:
            self.parser.error('You need to input a provider')

        # If local analysis, overwrite results
        if args.__dict__.get('fetch_local'):
            args.force_write = True

        # Test conditions
        v = vars(args)
        # AWS
        if v.get('provider') == 'aws':
            if v.get('aws_access_keys') and not (v.get('aws_access_key_id') or v.get('aws_secret_access_key')):
                self.parser.error('When running with --access-keys, you must provide an Access Key ID '
                                  'and Secret Access Key.')
        # Azure
        elif v.get('provider') == 'azure':
            if v.get('tenant_id') and not (v.get('service_principal') or v.get('user_account_browser')):
                self.parser.error('--tenant can only be set when using --user-account-browser or --service-principal authentication')
            if v.get('service_principal') and not v.get('tenant_id'):
                self.parser.error('You must provide --tenant when using --service-principal authentication')
            if v.get('user_account_browser') and not v.get('tenant_id'):
                self.parser.error('You must provide --tenant when using --user-account-browser authentication')
            if v.get('subscription_ids') and v.get('all_subscriptions'):
                self.parser.error('--subscription-ids and --all-subscriptions are mutually exclusive options')

        return args

