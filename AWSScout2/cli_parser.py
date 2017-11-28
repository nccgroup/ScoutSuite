#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opinel.utils.cli_parser import OpinelArgumentParser

from AWSScout2 import DEFAULT_REPORT_DIR



class SharedArgumentParser(OpinelArgumentParser):

    def __init__(self, default_args = None):
        super(SharedArgumentParser, self).__init__()
        self.add_argument('debug', default_args)
        self.add_argument('force', default_args)

    def add_argument(self, argument_name, default_args = None):
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

    def __init__(self, default_args = None):
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

    def __init__(self, default_args = None):
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



class Scout2ArgumentParser(SharedArgumentParser):

    def __init__(self, default_args = None):
        super(Scout2ArgumentParser, self).__init__()
        self.add_argument('profile', default_args)
        self.add_argument('regions', default_args)
        self.add_argument('vpc', default_args)
        self.add_argument('ip-ranges', default_args)
        self.add_argument('ip-ranges-name-key', default_args)
        self.add_argument('mfa-serial')
        self.add_argument('mfa-code')
        self.add_argument('csv-credentials')
        self.add_argument('report-dir', default_args)
        self.add_argument('timestamp', default_args)
        self.add_argument('exceptions', default_args)
        self.add_argument('services', default_args)
        self.add_argument('skip', default_args)
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
                                default=None,
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

    def parse_args(self):
        args = self.parser.parse_args()
        # If local analysis, overwrite results
        if args.fetch_local:
            args.force_write = True
        return args
