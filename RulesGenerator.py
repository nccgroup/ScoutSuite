#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *
from AWSScout2.findings import *

import json

########################################
##### Main
########################################

def main(args):

    # Configure the debug level
    configPrintException(args.debug)

    # Check arguments
    if args.ruleset_name[0] == 'default':
        printError('Error, you need to provide a name for your custom ruleset.')
        return

    # Create the list of services to customize
    services = build_services_list(args.services, args.skipped_services)
    if not len(services):
        printError('Error: list of Amazon Web Services to be analyzed is empty.')
        return

    # Load existing ruleset if editing one
    ruleset = load_ruleset(args.ruleset_name, quiet =  True)
    if not ruleset and False: # load default optionally
        ruleset = load_ruleset(['default'])
        printInfo('Creating a new ruleset, initiated with the default set.')
    elif not ruleset:
        # Initiate a new ruleset with all rules
        ruleset = {}
        ruleset['rules'] = []
        for rule in os.listdir('rules'):
            ruleset['rules'].append({'filename': rule})

    # Load rules metadata
    rules = init_rules(ruleset, services, args.ruleset_name[0], args.ip_ranges, generator = True)

    ruleset_new = {}
    ruleset_new['rules'] = []
    for resource_path in rules:
        for rule in rules[resource_path]:

            # Initialize rule metadata
            rule_metadata = {'filename': rules[resource_path][rule]['filename']}

            # Enable the rule ?
            verb = 'disable' if ('enabled' in rules[resource_path][rule] and rules[resource_path][rule]['enabled']) else 'enable'
            if prompt_4_yes_no('Do you want to %s the following rule:\n\t%s' % (verb, rules[resource_path][rule]['description'])):
                enabled = True if verb == 'enable' else False
            else:
                enabled = False if verb == 'enable' else True

            # Set the rule's arguments
            if enabled and verb == 'disable' and 'questions' in rules[resource_path][rule]:
                configure = prompt_4_yes_no('Do you want to change the parameters for this rule')
                if not configure:
                    rule_metadata['args'] = rules[resource_path][rule]['args']
            elif enabled and verb == 'enable' and 'questions' in rules[resource_path][rule]:
                configure = True
            else:
                configure = False
            rule_metadata['enabled'] = enabled
            if configure:
                question_args = []
                for question_id, question in enumerate(rules[resource_path][rule]['questions']):
                    try:
                        choices = []
                        all_choices = []
                        for choice in rules[resource_path][rule]['questions'][question_id][1]:
                            choice = ast.literal_eval(choice)
                            if type(choice) == tuple:
                                choices.append(choice[0])
                                all_choices.append(choice)
                                answer_next = True
                    except:
                        choices = rules[resource_path][rule]['questions'][question_id][1]
                    arg_value = prompt_4_value(rules[resource_path][rule]['questions'][question_id][0], choices = choices, default = rules[resource_path][rule]['questions'][question_id][2], is_question = True)             
                    if answer_next:
                        for choice in all_choices:
                            if choice[0] == arg_value:
                                for i, v in enumerate(choice):
                                    question_args.append(v)
                                break
                    else:
                        question_args.append(arg_value)
                rule_metadata['args'] = question_args
            ruleset_new['rules'].append(rule_metadata) 


    # Save ruleset
    with open('rulesets/%s.json' % args.ruleset_name[0], 'wt') as f:
        f.write(json.dumps(ruleset_new, indent = 4, sort_keys = True))

    return


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
add_common_argument(parser, default_args, 'ip-ranges')

parser.add_argument('--all',
                    dest='review_defaults',
                    default=False,
                    action='store_true',
                    help='review and customize all rules, including the default ruleset')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
