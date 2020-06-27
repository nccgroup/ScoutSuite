#!/usr/bin/env python

import os

scout_dir = 'ScoutSuite'
tests_dir = 'testsbase'

for root, dirnames, filenames in os.walk(scout_dir):
    for filename in filenames:
        if filename.startswith('__') or not filename.endswith('.py'):
            continue
        filepath = os.path.join(root, filename)
        tmp = filepath.split('.')[0].split('/')
        print(str(tmp))

        test = '# Import AWS utils\nfrom {} import *\n\n#\n# Test methods for {}\n#\n\nclass Test{}Class:\n\n'.format('.'.join(tmp), filepath, ''.join(t.title() for t in tmp))

        test_filename = 'test-%s.py' % '-'.join(tmp[1:])
        print(f'{filepath} --> {test_filename}')
        test_file = os.path.join(tests_dir, test_filename)
        if not os.path.isfile(test_file):
            with open(test_file, 'w+') as f:
                f.write(test)

