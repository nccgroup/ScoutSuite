#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ScoutSuite.__listall__ import main as listall
from ScoutSuite.__rules_generator__ import main as rules_generator
from ScoutSuite.__main__ import main as scout

from ScoutSuite.cli_parser import ScoutSuiteArgumentParser

if __name__ == "__main__":
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()
    if args.module == "listall":
        main = listall
    elif args.module == "rules":
        main = rules_generator
    else:
        main = scout
    sys.exit(main(args))
