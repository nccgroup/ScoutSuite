#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *


########################################
##### Main
########################################

def main(args):

    # Create the list of services to customize
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        print 'Error: list of Amazon Web Services to be analyzed is empty.'
        return

    for service in supported_services:
        if service not in services:
            # For services not customized, enable all default rules
            load_findings(service, 'default')

    for service in services:
        if not args.review_defaults:
            # By default, enable all default rules
            load_findings(service, 'default')
        else:
            # Otherwise, all rules that have "questions" key will be reviewed
            load_findings(service, 'default', True)

        # Select custom rules
        load_findings(service, 'custom')

    # Save new ruleset
    for service in supported_services:
        ruleset = globals()[service + '_finding_dictionary']
        filename = 'rules/findings-' + service + '.' + args.ruleset_name[0] + '.json'
        save_blob_to_file(filename, ruleset, args.force_write)


########################################
##### Argument parser
########################################

parser.add_argument('--all',
                    dest='review_defaults',
                    default=False,
                    action='store_true',
                    help='review and customize all rules, including the default ruleset')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
