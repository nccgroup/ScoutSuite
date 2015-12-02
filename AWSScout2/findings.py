# Import AWS Scout2 finding-related classes
from AWSScout2.finding_cloudtrail import *
from AWSScout2.finding_ec2 import *
from AWSScout2.finding_iam import *
from AWSScout2.finding_rds import *
from AWSScout2.finding_redshift import *
from AWSScout2.finding_s3 import *
from AWSScout2.utils import *

# Import opinel
from opinel.utils import *

# Import stock packages
import copy
import fnmatch
import os
import re


########################################
# Finding dictionaries
########################################
cloudtrail_finding_dictionary = {}
iam_finding_dictionary = {}
ec2_finding_dictionary = {}
rds_finding_dictionary = {}
redshift_finding_dictionary = {}
s3_finding_dictionary = {}

finding_levels = ['danger', 'warning']

########################################
# Common functions
########################################

def change_level(level):
    if prompt_4_yes_no('Would you like to change the default level (%s)' % level):
        return prompt_4_value('Enter the level: ', finding_levels, level)
    else:
        return level

#
# Load rule from a JSON config file
#
def load_config_from_json(rule_metadata, environment_name, ip_ranges):
    config = None
    config_file = 'rules_new/%s' % rule_metadata['filename']
    config_args = rule_metadata['args'] if 'args' in rule_metadata else []
    try:
        with open(config_file, 'rt') as f:
            config = f.read()
        # Replace arguments
        for idx, argument in enumerate(config_args):
            config = config.replace('_ARG_'+str(idx)+'_', argument.strip())
        config = json.loads(config)
        # Load lists from files
        for c1 in config['conditions']:
            if ((type(c1[2]) == str) or (type(c1[2]) == unicode)):
                values = re_ip_ranges_from_file.match(c1[2])
                if values:
                    filename = values.groups()[0]
                    conditions = json.loads(values.groups()[1])
                    if filename == aws_ip_ranges:
                        filename = filename.replace('_PROFILE_', environment_name)
                        c1[2] = read_ip_ranges(filename, False, conditions, True)
                    elif filename == ip_ranges_from_args:
                        c1[2] = []
                        for ip_range in ip_ranges:
                            c1[2] = c1[2] + read_ip_ranges(ip_range, True, conditions, True)
        # Set condition operator
        if not 'condition_operator' in config:
            config['condition_operator'] = 'and'
        # Fix level if specified in ruleset
        if 'level' in rule_metadata:
            rule['level'] = rule_metadata['level']
    except Exception as e:
        printException(e)
        printError('Error: failed to read the rule from %s' % config_file)
    return config

#
# Load a ruleset from a JSON file
#
def load_ruleset(ruleset_name):
    ruleset_filename = 'rulesets/%s.json' % ruleset_name[0]
    if not os.path.exists(ruleset_filename):
        printError('Error: the ruleset name entered (%s) does not match an existing configuration.' % ruleset_name[0])
        return None
    try:
        with open(ruleset_filename, 'rt') as f:
            ruleset = json.load(f)
    except Exception as e:
        printException(e)
        printError('Error: ruleset file %s contains malformed JSON.' % ruleset_filename)
        return None
    return ruleset

def init_rules(ruleset, services, environment_name, ip_ranges):
    # Load rules from JSON files
    rules = {}
    for rule_metadata in ruleset['rules']:
        # Skip disabled rules
        if 'enabled' in rule_metadata and rule_metadata['enabled'] in ['false', 'False']:
            continue
        # Skip rules that apply to an out-of-scope service
        rule_details = load_config_from_json(rule_metadata, environment_name, ip_ranges)
        skip_rule = True
        for service in services:
            if rule_details['entities'].startswith(service):
                skip_rule = False
        if skip_rule:
            continue
        # Build the rules dictionary
        entities = rule_details.pop('entities')
        manage_dictionary(rules, entities, {})
        if 'level' in rule_metadata:
            rule_details['level'] = rule_metadata['level']
        key = rule_details['key'] if 'key' in rule_details else rule_metadata['filename']
        # Set condition operator
        if not 'condition_operator' in rule_details:
            rule_details['condition_operator'] = 'and'
        # Save details for rule
        rules[entities][key] = rule_details
    return rules

    # Parse and customize rules
    for f in findings:
        questions = findings[f]['questions'] if 'questions' in findings[f] else []
        if 'targets' in findings[f]:
            for t in findings[f]['targets']:
                name = set_argument_values(f, t)
                description = set_argument_values(findings[f]['description'], t)
                entity = set_argument_values(findings[f]['entity'], t)
                callback = findings[f]['callback']
                callback_args = set_arguments(findings[f]['callback_args'], t)
                level = set_argument_values(findings[f]['level'], t)
                new_questions = []
                for q in questions:
                    if type(q) == list:
                        new_questions.append([set_argument_values(q[0], t)] + q[1:])
                    else:
                        new_questions.append(set_argument_values(q, t))

                new_finding(service, customize, name,
                    description,
                    entity,
                    callback,
                    callback_args,
                    level,
                    new_questions)

        else:
            update_ruleset(findings[f])

            new_finding(service, customize, f,
                findings[f]['description'],
                findings[f]['entities'],
                findings[f]['conditions'],
                findings[f]['level'],
                questions)

def new_finding(service, customize, key, description, entity, callback_name, level, questions):

    # Based on the service name, determine the finding dictionary and class
    finding_dictionary, finding_class = get_finding_variables(service)

    # If this is a custom rule, prompt users for answers
    if customize and questions and len(questions):
        print('')
        activate_rule_question = set_description(questions.pop(0), description)
        if prompt_4_yes_no(activate_rule_question):
            for question in questions:
                if type(question) == list:
                    if len(question) == 2:
                        q, choices = question
                        default = None
                    elif len(question) == 3:
                        q, choices, default = question
                else:
                    q = question
                    choices = None
                    default = None
                answer = prompt_4_value(q, choices, default, is_question = True)
                callback_args.append(answer)
            level = change_level(level)
        else:
            return

    # Save the rule in the finding dictionary
    finding_dictionary[key] = finding_class(description, entity, callback_name, level, questions)

#
# Search for an existing ruleset that matches the environment name
#
def search_ruleset(environment_name):
    if environment_name != 'default':
        ruleset_found = False
        for f in os.listdir('rulesets'):
            if fnmatch.fnmatch(f, '*.' + environment_name + '.json'):
                ruleset_found = True
        if ruleset_found and prompt_4_yes_no("A ruleset whose name matches your environment name (%s) was found. Would you like to use it instead of the default one" % environment_name):
            return environment_name
    return 'default'

def set_arguments(arg_names, t):
    real_args = []
    for a in arg_names:
        real_args.append(set_argument_values(a, t))
    return real_args

def set_argument_values(string, target):
    args = re.findall(r'(_ARG_(\w+)_)', string)
    for arg in args:
        index = int(arg[1])
        string = string.replace(arg[0], target[index])
    return string

def set_description(string, description):
    attributes = re.findall(r'(_(\w+)_)', string)
    for attribute in attributes:
        name = attribute[1].lower()
        if name == 'description':
            string = string.replace(attribute[0], description)
        else:
            printError('The field %s is not supported yet for injection in the questions')
    return string

def get_finding_variables(keyword):
    if keyword == 'ec2':
        return ec2_finding_dictionary, Ec2Finding
    elif keyword == 'iam':
        return iam_finding_dictionary, IamFinding
    elif keyword == 's3':
        return s3_finding_dictionary, S3Finding
    elif keyword == 'cloudtrail':
        return cloudtrail_finding_dictionary, CloudTrailFinding
    elif keyword == 'rds':
        return rds_finding_dictionary, RdsFinding
    elif keyword == 'redshift':
        return redshift_finding_dictionary, RedshiftFinding
    else:
        return None, None
