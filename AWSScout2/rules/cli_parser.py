#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AWSScout2 import DEFAULT_REPORT_DIR
from opinel.cli_parser import OpinelArgumentParser


class RulesArgumentParser(OpinelArgumentParser):
    """

    """

    def __init__(self, default_args = None):
        super(RulesArgumentParser, self).__init__()
        self.add_argument('debug', default_args)
        self.add_argument('profile', default_args)
        self.add_argument('force', default_args)
        self.parser.add_argument('--ruleset-name',
                                dest='ruleset_name',
                                default=None,
                                required=True,
                                help='Load settings from an existing ruleset.')
        self.parser.add_argument('--base-ruleset',
                                dest='base_ruleset',
                                default='default',
                                help='Name of the ruleset to be generated.')
        self.parser.add_argument('--rules-dir',
                                 dest='rules_dir',
                                 default=[],
                                 nargs='+',
                                 help='Path to custom rules.')
        self.parser.add_argument('--output-dir',
                                 dest='output_dir',
                                 default=DEFAULT_REPORT_DIR,
                                 help='Name / Path')

    def parse_args(self):
        args = self.parser.parse_args()
        return args