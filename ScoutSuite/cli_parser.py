#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from opinel.utils.cli_parser import OpinelArgumentParser

from ScoutSuite import DEFAULT_REPORT_DIR


class SharedArgumentParser(OpinelArgumentParser):

    def __init__(self, default_args=None):
        super(SharedArgumentParser, self).__init__()
        self.add_argument('debug', default_args)
        self.add_argument('force', default_args)

    def add_argument(self, argument_name, default_args=None):
        if argument_name == 'services':
            self.parser.add_argument('--services',
                                     dest='services',
                                     default=[],
                                     nargs='+',
                                     help='Name of in-scope services.')
        elif argument_name == 'skip':
            self.parser.add_argument('--skip',
                                     dest='skipped_services',
                                     default=[],
                                     nargs='+',
                                     help='Name of out-of-scope services.')
        elif argument_name == 'timestamp':
            self.parser.add_argument('--timestamp',
                                     dest='timestamp',
                                     default=False,
                                     nargs='?',
                                     help='Timestamp added to the name of the report (default is current time in UTC).')
        elif argument_name == 'report-dir':
            self.parser.add_argument('--report-dir',
                                     dest='report_dir',
                                     default=DEFAULT_REPORT_DIR,
                                     help='Path of the Scout2 report.')
        elif argument_name == 'exceptions':
            self.parser.add_argument('--exceptions',
                                     dest='exceptions',
                                     default=[None],
                                     nargs='+',
                                     help='Exception file to use during analysis.')
        else:
            super(SharedArgumentParser, self).add_argument(argument_name, default_args)


class RulesArgumentParser(SharedArgumentParser):

    def __init__(self, default_args=None):
        super(RulesArgumentParser, self).__init__()
        self.parser.add_argument('--ruleset-name',
                                 dest='ruleset_name',
                                 default=None,
                                 required=True,
                                 help='Name of the ruleset to be generated.')
        self.parser.add_argument('--base-ruleset',
                                 dest='base_ruleset',
                                 default='default',
                                 help='Ruleset to be used as the baseline.')
        self.parser.add_argument('--rules-dir',
                                 dest='rules_dir',
                                 default=[],
                                 nargs='+',
                                 help='Path to directories where custom rules are defined.')
        self.parser.add_argument('--generator-dir',
                                 dest='generator_dir',
                                 default=DEFAULT_REPORT_DIR,
                                 help='Path of the Scout2 rules generator.')
        self.parser.add_argument('--no-browser',
                                 dest='no_browser',
                                 default=False,
                                 action='store_true',
                                 help='Do not automatically open the report in the browser.')


class ListallArgumentParser(SharedArgumentParser):

    def __init__(self, default_args=None):
        super(ListallArgumentParser, self).__init__()
        self.add_argument('profile', default_args)
        self.add_argument('report-dir', default_args)
        self.add_argument('ip-ranges', default_args)
        self.add_argument('timestamp', default_args)
        self.add_argument('exceptions', default_args)
        self.parser.add_argument('--format',
                                 dest='format',
                                 default=['csv'],
                                 nargs='+',
                                 help='Listall output format.')
        self.parser.add_argument('--format-file',
                                 dest='format_file',
                                 default=None,
                                 nargs='+',
                                 help='Listall output format file')
        self.parser.add_argument('--config',
                                 dest='config',
                                 default=None,
                                 help='Config file that sets the path and keys to be listed.')
        self.parser.add_argument('--config-args',
                                 dest='config_args',
                                 default=[],
                                 nargs='+',
                                 help='Arguments to be passed to the config file.')
        self.parser.add_argument('--path',
                                 dest='path',
                                 default=[],
                                 nargs='+',
                                 help='Path of the resources to list (e.g. iam.users.id or ec2.regions.id.vpcs.id)')
        self.parser.add_argument('--keys',
                                 dest='keys',
                                 default=[],
                                 nargs='+',
                                 help='Keys to be printed for the given object.')
        self.parser.add_argument('--keys-from-file',
                                 dest='keys_file',
                                 default=[],
                                 nargs='+',
                                 help='Keys to be printed for the given object (read values from file.')


class ScoutSuiteArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(title="The provider you want to run Scout against",
                                                dest="provider")

        # Global settings
        self.parser.add_argument('--debug',
                                 dest='debug',
                                 default=False,
                                 action='store_true',
                                 help='Print the stack trace when exception occurs')
        self.parser.add_argument('-l', '--local',
                                 dest='fetch_local',
                                 default=False,
                                 action='store_true',
                                 help='Use local data previously fetched and re-run the analysis.')
        self.parser.add_argument('--resume',
                                 dest='resume',
                                 default=False,
                                 action='store_true',
                                 help='Complete a partial (throttled) run')
        self.parser.add_argument('--update',
                                 dest='update',
                                 default=False,
                                 action='store_true',
                                 help='Reload all the existing data and only overwrite data in scope for this run')
        self.parser.add_argument('--ruleset',
                                 dest='ruleset',
                                 default='default.json',
                                 nargs='?',
                                 help='Set of rules to be used during the analysis.')
        self.parser.add_argument('--no-browser',
                                 dest='no_browser',
                                 default=False,
                                 action='store_true',
                                 help='Do not automatically open the report in the browser.')
        self.parser.add_argument('--thread-config',
                                 dest='thread_config',
                                 type=int,
                                 default=4,
                                 help='Level of multi-threading wanted [1-5]; defaults to 4.')
        self.parser.add_argument('--report-dir',
                                 dest='report_dir',
                                 default=DEFAULT_REPORT_DIR,
                                 help='Path of the Scout2 report.')
        self.parser.add_argument('--timestamp',
                                 dest='timestamp',
                                 default=False,
                                 nargs='?',
                                 help='Timestamp added to the name of the report (default is current time in UTC).')
        self.parser.add_argument('--exceptions',
                                 dest='exceptions',
                                 default=[None],
                                 nargs='+',
                                 help='Exception file to use during analysis.')
        self.parser.add_argument('--force',
                                 dest='force_write',
                                 default=False,
                                 action='store_true',
                                 help='Overwrite existing files')

        # Amazon Web Services
        aws_parser = subparsers.add_parser("aws",
                                           help="Run Scout against an Amazon web Services account")

        default = os.environ.get('AWS_PROFILE', 'default')
        default_origin = " (from AWS_PROFILE)." if 'AWS_PROFILE' in os.environ else "."
        aws_parser.add_argument('--profile',
                                dest='profile',
                                default=[default],
                                nargs='+',
                                help='Name of the profile. Defaults to %(default)s' + default_origin)
        aws_parser.add_argument('--regions',
                                dest='regions',
                                default=[],
                                nargs='+',
                                help='Name of regions to run the tool in, defaults to all')
        aws_parser.add_argument('--vpc',
                                dest='vpc',
                                default=[],
                                nargs='+',
                                help='Name of VPC to run the tool in, defaults to all')
        aws_parser.add_argument('--ip-ranges',
                                dest='ip_ranges',
                                default=[],
                                nargs='+',
                                help='Config file(s) that contain your known IP ranges')
        aws_parser.add_argument('--ip-ranges-name-key',
                                dest='ip_ranges_name_key',
                                default='name',
                                help='Name of the key containing the display name of a known CIDR')
        aws_parser.add_argument('--mfa-serial',
                                dest='mfa_serial',
                                default=None,
                                help='ARN of the user\'s MFA device')
        aws_parser.add_argument('--mfa-code',
                                dest='mfa_code',
                                default=None,
                                help='Six-digit code displayed on the MFA device.')
        aws_parser.add_argument('--csv-credentials',
                                dest='csv_credentials',
                                default=None,
                                help='Path to a CSV file containing the access key ID and secret key')
        aws_parser.add_argument('--services',
                                dest='services',
                                default=[],
                                nargs='+',
                                help='Name of in-scope services.')
        aws_parser.add_argument('--skip',
                                dest='skipped_services',
                                default=[],
                                nargs='+',
                                help='Name of out-of-scope services.')

        # Google Cloud Platform
        gcp_parser = subparsers.add_parser("gcp",
                                           help="Run Scout against a Google Cloud Platform account")

        gcp_auth_modes = gcp_parser.add_mutually_exclusive_group(required=True)

        gcp_auth_modes.add_argument('--user-account',
                                    action='store_true',
                                    dest="auth_file",
                                    help='Run Scout Suite with a Google Account')

        gcp_auth_modes.add_argument('--service-account',
                                    action='store',
                                    help='Run Scout Suite with a Google Service Account with the specified '
                                         'Google Service Account Application Credentials file')

        gcp_scope = gcp_parser.add_mutually_exclusive_group(required=False)

        gcp_scope.add_argument('--project-id',
                               action='store',
                               help='ID of the GCP Project to analyze')

        gcp_scope.add_argument('--folder-id',
                               action='store',
                               help='ID of the GCP Folder to analyze')

        gcp_scope.add_argument('--organization-id',
                               action='store',
                               help='ID of the GCP Organization to analyze')

        # Microsoft Azure
        azure_parser = subparsers.add_parser("azure",
                                             help="Run Scout against a Microsoft Azure account")

        azure_auth_modes = azure_parser.add_mutually_exclusive_group(required=True)

        azure_auth_modes.add_argument('--cli',
                                      action='store_true',
                                      help='Run Scout Suite using configured azure-cli credentials')

        azure_auth_modes.add_argument('--msi',
                                      action='store_true',
                                      help='Run Scout Suite with Managed Service Identity')

        azure_auth_modes.add_argument('--service-principal',
                                      action='store_true',
                                      help='Run Scout Suite with an Azure Service Principal')

        azure_auth_modes.add_argument('--file-auth',
                                      action='store',
                                      dest='auth_file',
                                      help='Run Scout Suite with the specified credential file')

        azure_auth_modes.add_argument('--user-credentials',
                                      action='store_true',
                                      help='Run Scout Suite with user credentials')

    def parse_args(self, args=None):
        args = self.parser.parse_args(args)
        # If local analysis, overwrite results
        if args.fetch_local:
            args.force_write = True
        return args
