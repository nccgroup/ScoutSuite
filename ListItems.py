#!/usr/bin/env python2

# Import AWS Scout2 tools
from AWSScout2.utils import *

# Import third-party packages
from collections import OrderedDict


########################################
##### Main
########################################

def main(args):

    # Configure the debug level
    configPrintException(args.debug)

    # Get the environment name
    environment_name = get_environment_name(args)

    # Create the list of services to analyze
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        print 'Error: list of Amazon Web Services to be analyzed is empty.'
        return

    # Load the data
    violations = OrderedDict()
    for service in services:
        try:
            data = load_info_from_json(service, environment_name)
            violations.update(data['violations'])
        except Exception, e:
            printException(e)

    # Let users pick the violation to dump the items for
    violation_name = args.violation_name[0]
    if not violation_name:
        violation_names = violations.keys()
        for v in violation_names:
            print '%3d. %s - %s' % (violation_names.index(v), violations[v]['keyword_prefix'].upper(), v)
        indices = [ '%d' % i for i in range(0, len(violations)) ]
        choices = prompt_4_value('Which violation ID do you want to output the items for', indices, display_choices = False, authorize_list = True)

    # Dump the list of items
    output = ''
    choices = choices.split(',')
    for c in choices:
        violation_name = violation_names[int(c)]
        violation = violations[violation_name]
        if len(violation['items']) == len(violation['macro_items']):
            for item, macro_item in zip(violation['items'], violation['macro_items']):
                output = output + '%s : %s\n' % (macro_item, item)
        else:
            for item in violation['items']:
                output = output + '%s\n' % item

    # Output
    if args.output_file[0]:
        try:
            f = open(args.output_file[0], 'wt')
            f.write(output)
            f.close()
        except Exception, e:
            printException(e)
    else:
        print output


########################################
##### Argument parser
########################################

parser.add_argument('--env',
                    dest='environment_name',
                    default=None,
                    nargs='+',
                    help='AWS environment name (used to create multiple reports)')
parser.add_argument('--out',
                    dest='output_file',
                    default=[ None ],
                    nargs='+',
                    help='Name of the output file.')
parser.add_argument('--violation_name',
                    dest='violation_name',
                    default=[ None ],
                    nargs='+',
                    help='Name (key) of the violation to get the items from')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
