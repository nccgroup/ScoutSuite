#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opinel.cli_parser import OpinelArgumentParser
from AWSScout2 import DEFAULT_REPORT_DIR

class ListallArgumentParser(OpinelArgumentParser):
    """

    """

    def __init__(self, default_args = None):
        super(ListallArgumentParser, self).__init__()
        self.add_argument('debug', default_args)
        self.add_argument('profile', default_args)

        self.parser.add_argument('--format',
                                    dest='format',
                                    default=['csv'],
                                    nargs='+',
                                    help='Listall output format')
        self.parser.add_argument('--format-file',
                                dest='format_file',
                                default=None,
                                nargs='+',
                                help='Listall output format file')
        self.parser.add_argument('--timestamp',
                                 dest='timestamp',
                                 default=False,
                                 nargs='?',
                                 help='Add a timestamp to the name of the report (default is current time in UTC)')

        self.parser.add_argument('--config',
                            dest='config',
                            default=None,
                            help='Config file that sets the path and keys to be listed.')
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
        self.parser.add_argument('--ip-ranges',
                            dest='ip_ranges',
                            default=[],
                            nargs='+',
                            help='Config file(s) that contain your own IP ranges.')
        self.parser.add_argument('--config-args',
                            dest='config_args',
                            default=[],
                            nargs='+',
                            help='Arguments to be passed to the config file.')
        self.parser.add_argument('--report-dir',
                                 dest='report_dir',
                                 default=DEFAULT_REPORT_DIR,
                                 help='Name / Path')

    def parse_args(self):
        args = self.parser.parse_args()
        return args



class Scout2ArgumentParser(OpinelArgumentParser):
    """

    """

    def __init__(self, default_args = None):
        super(Scout2ArgumentParser, self).__init__()
        self.add_argument('debug', default_args)
        self.add_argument('profile', default_args)
        self.add_argument('regions', default_args)
        self.add_argument('partition-name', default_args)
        self.add_argument('vpc', default_args)
        self.add_argument('force', default_args)
        self.add_argument('ip-ranges', default_args)
        self.add_argument('ip-ranges-key-name', default_args)
        self.add_argument('mfa-serial')
        self.add_argument('mfa-code')
        self.add_argument('csv-credentials')
        self.parser.add_argument('-l', '--local',
                                dest='fetch_local',
                                default=False,
                                action='store_true',
                                help='Use local data previously fetched and re-run the analyzis.')
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
        self.parser.add_argument('--exceptions',
                                dest='exceptions',
                                default=[None],
                                nargs='+',
                                help='')
        self.parser.add_argument('--timestamp',
                                dest='timestamp',
                                default=False,
                                nargs='?',
                                help='Add a timestamp to the name of the report (default is current time in UTC)')
        self.parser.add_argument('--output-dir',
                                dest='report_dir',
                                default=DEFAULT_REPORT_DIR,
                                nargs='?',
                                help='Name / Path')
        self.parser.add_argument('--ruleset',
                                dest='ruleset',
                                default=None,
                                nargs='?',
                                help='Customized set of rules')
        self.parser.add_argument('--services',
                                dest='services',
                                default=[],
                                nargs='+',
                                help='Name of the Amazon Web Services you want to work with')
        self.parser.add_argument('--skip',
                                dest='skipped_services',
                                default=[],
                                nargs='+',
                                help='Name of services you want to ignore')



    def parse_args(self):
        args = self.parser.parse_args()

        #args = super(Scout2ArgumentParser, self).parser.parse_args()
        # If local analysis, overwrite results
        if args.fetch_local:
            args.force_write = True

        # Prepare the output folder
        print(args.report_dir)

        return args
