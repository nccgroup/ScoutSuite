#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import asyncio

from ScoutSuite.__main__ import main as scout
from ScoutSuite.cli_parser import ScoutSuiteArgumentParser

if __name__ == "__main__":
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scout(args))
    loop.close()
    sys.exit()
