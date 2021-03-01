#!/usr/bin/env python3

import sys

from ScoutSuite.__main__ import run_from_cli

if __name__ == "__main__":
    sys.argv = ['scout.py', 'azure', '--cli', '--force']
    sys.exit(run_from_cli())
