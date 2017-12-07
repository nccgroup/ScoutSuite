#!/usr/bin/env python

import json
import os
import re
import sys

if len(sys.argv) < 2:
    print('Error, you must provide the path to the ruleset as an argument.\nUsage:\n$ sort-ruleset.py <path_to_filename.json>\n')
    sys.exit(42)

ruleset_name = sys.argv[1]
if not os.path.isfile(ruleset_name):
    print('Error, the path provided is not valid.')
    sys.exit(42)

with open(ruleset_name, 'rt') as f:
    ruleset = json.load(f)

ruleset = json.dumps(ruleset, indent = 4, sort_keys = True)


with open(ruleset_name, 'wt') as f:
    for line in ruleset.split('\n'):
        f.write('%s\n' % line.rstrip())
