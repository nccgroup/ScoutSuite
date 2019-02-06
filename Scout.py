#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ScoutSuite.__listall__ import main as listall
from ScoutSuite.__rules_generator__ import main as rules_generator
from ScoutSuite.__main__ import main as scout

from ScoutSuite.cli_parser import ScoutSuiteArgumentParser

modules = {
    "listall": listall,
    "ruleset": rules_generator,
}

if __name__ == "__main__":
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    sys.exit(modules.get(args.module, scout)(args))
