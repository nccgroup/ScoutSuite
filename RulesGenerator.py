#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *

# Import other third-party packages
import argparse


########################################
##### Main
########################################

def main(args):

    for service in supported_services:
        if not args.review_defaults:
            # By default, enable all default rules
            load_findings(service, 'default')
        else:
            # Otherwise, all rules that have "questions" key will be reviewed
            load_findings(service, 'default', True)

    # Select custom rules
    for service in supported_services:
        load_findings(service, 'custom')

    # Save new ruleset
    for service in supported_services:
        ruleset = globals()[service + '_finding_dictionary']
        filename = 'rules/findings-' + service + '.' + args.ruleset_name[0] + '.json'
        save_blob_to_file(filename, ruleset, args.force_write)


########################################
##### Argument parser
########################################
parser = argparse.ArgumentParser()
parser.add_argument('--all',
                    dest='review_defaults',
                    default=False,
                    action='store_true',
                    help='review and customize all rules, including the default ruleset')
parser.add_argument('--force',
                    dest='force_write',
                    default=False,
                    action='store_true',
                    help='overwrite existing json files')
parser.add_argument('--ruleset_name',
                    dest='ruleset_name',
                    required=True,
                    nargs='+',
                    help='name of the custom ruleset')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
