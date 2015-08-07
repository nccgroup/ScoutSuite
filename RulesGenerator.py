#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *


########################################
##### Main
########################################

def main(args):

    # Configure the debug level
    configPrintException(args.debug)

    # Check arguments
    if args.ruleset_name == 'default':
        printError('Error, you need to provide a name for your custom ruleset.')
        return

    # Create the list of services to customize
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        printError('Error: list of Amazon Web Services to be analyzed is empty.')
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
        save_blob_to_file(filename, ruleset, args.force_write, args.debug)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_scout2_argument(parser, default_args, 'force')
add_scout2_argument(parser, default_args, 'ruleset-name')
add_scout2_argument(parser, default_args, 'services')
add_scout2_argument(parser, default_args, 'skip')

parser.add_argument('--all',
                    dest='review_defaults',
                    default=False,
                    action='store_true',
                    help='review and customize all rules, including the default ruleset')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
