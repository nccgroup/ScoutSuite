#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opinel.cli_parser import OpinelArgumentParser
import os
import zipfile



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
        self.parser.add_argument('--report-dir',
                                dest='report_dir',
                                default=None,
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
        self.parser.add_argument('--env',
                                dest='environment_name',
                                default=[],
                                nargs='+',
                                help='AWS environment name (used when working with multiple reports)')

    def parse_args(self):
        args = super(Scout2ArgumentParser, self).parse_args()
        # If local analysis, overwrite results
        if args.fetch_local:
            args.force_write = True

        # Prepare the output folder
        print(args.report_dir)

        return args
