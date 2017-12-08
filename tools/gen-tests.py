#!/usr/bin/env python

import os

scout2_dir = 'AWSScout2'
tests_dir = 'testsbase'

for root, dirnames, filenames in os.walk(scout2_dir):
    for filename in filenames:
        if filename.startswith('__') or not filename.endswith('.py'):
            continue
        filepath = os.path.join(root, filename)
        tmp = filepath.split('.')[0].split('/')
        print(str(tmp))

        test = '# Import AWS utils\nfrom %s import *\n\n#\n# Test methods for %s\n#\n\nclass Test%sClass:\n\n' % ('.'.join(tmp), filepath, ''.join(t.title() for t in tmp))

        test_filename = 'test-%s.py' % '-'.join(tmp[1:])
        print('%s --> %s' % (filepath, test_filename))
        test_file = os.path.join(tests_dir, test_filename)
        if not os.path.isfile(test_file):
            with open(test_file, 'w+') as f:
                f.write(test)

