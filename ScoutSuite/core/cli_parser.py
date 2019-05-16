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

    def _init_aws_parser(self):
        aws_parser = self.subparsers.add_parser("aws",
                                                parents=[self.common_providers_args_parser],
                                                help="Run Scout against an Amazon Web Services account")

        parser = aws_parser.add_argument_group('Authentication parameters')

        parser.add_argument('-p',
                            '--profile',
                            dest='profile',
                            default=None,
                            help='Name of the profile')

        parser = aws_parser.add_argument_group('Additional arguments')

        parser.add_argument('-r',
                            '--regions',
                            dest='regions',
                            default=[],
                            nargs='+',
                            help='Name of regions to run the tool in, defaults to all')
        parser.add_argument('--ip-ranges',
                            dest='ip_ranges',
                            default=[],
                            nargs='+',
                            help='Config file(s) that contain your known IP ranges')
        parser.add_argument('--ip-ranges-name-key',
                            dest='ip_ranges_name_key',
                            default='name',
                            help='Name of the key containing the display name of a known CIDR')

    def _init_gcp_parser(self):
        gcp_parser = self.subparsers.add_parser("gcp",
                                                parents=[self.common_providers_args_parser],
                                                help="Run Scout against a Google Cloud Platform account")

        parser = gcp_parser.add_argument_group('Authentication modes')
        gcp_auth_modes = parser.add_mutually_exclusive_group(required=True)

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

        gcp_scope = gcp_parser.add_argument_group('Additional arguments')

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

        azure_auth_modes.add_argument('-c',
                                      '--cli',
                                      action='store_true',
                                      help='Run Scout using configured azure-cli credentials')

        azure_auth_modes.add_argument('-m',
                                      '--msi',
                                      action='store_true',
                                      help='Run Scout with Managed Service Identity')

        azure_auth_modes.add_argument('-s',
                                      '--service-principal',
                                      action='store_true',
                                      help='Run Scout with an Azure Service Principal')
        azure_auth_params.add_argument('--tenant',
                                       action='store',
                                       dest='tenant_id',
                                       help='Tenant ID of the service principal')
        azure_auth_params.add_argument('--subscription',
                                       action='store',
                                       dest='subscription_id',
                                       help='Subscription ID of the service principal')
        azure_auth_params.add_argument('--client-id',
                                       action='store',
                                       dest='client_id',
                                       help='Client ID of the service principal')
        azure_auth_params.add_argument('--client-secret',
                                       action='store',
                                       dest='client_secret',
                                       help='Client of the service principal')

        azure_auth_modes.add_argument('--file-auth',
                                      action='store',
                                      type=argparse.FileType('r'),
                                      dest='file_auth',
                                      metavar="FILE",
                                      help='Run Scout with the specified credential file')

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
                            help='Maximum number of threads (workers) used by Scout Suite')
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
                            help='Name of in-scope services.')
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
                            help="Serve the specified result database on the server to show the report. "
                                 "This must be used when the results are exported as an sqlite database.")
        parser.add_argument('--host',
                            dest="host_ip",
                            default="127.0.0.1",
                            help="Address on which you want the server to listen. Defaults to localhost.")
        parser.add_argument('--port',
                            dest="host_port",
                            type=int,
                            default=8000,
                            help="Port on which you want the server to listen. Defaults to 8000.")

    def parse_args(self, args=None):
        args = self.parser.parse_args(args)

        # Cannot simply use required for backward compatibility
        if not args.provider:
            self.parser.error('You need to input a provider')
        # If local analysis, overwrite results
        if args.__dict__.get('fetch_local'):
            args.force_write = True
        return args
