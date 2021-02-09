#!/usr/bin/env python3

import sys

from ScoutSuite.__main__ import run_from_cli

if __name__ == "__main__":
    sys.argv = ['scout.py', 'azure', '--cli', '--force']
    # sys.argv = ['scout.py', 'azure', '--user-account', '--force']

    # sys.argv = ['scout.py', 'azure', '--user-account-browser', '--force', '--tenant',
    #             '0cc90829-0d8e-40d6-ba9c-aea092ba7de5']
    sys.exit(run_from_cli())
