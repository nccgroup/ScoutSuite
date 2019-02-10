#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ScoutSuite.__main__ import main as scout
from ScoutSuite.cli_parser import ScoutSuiteArgumentParser

if __name__ == "__main__":
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    sys.exit(scout(args))
