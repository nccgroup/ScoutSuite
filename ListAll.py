#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *

# Import third-party packages
import datetime
import dateutil.parser
import re
import sys


########################################
##### Config file
########################################

class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)

#
# Read arguments from a config file
#
def read_dump_config(config_file):
    config = None
    try:
        with open(config_file, 'rt') as f:
            config = json.load(f)
    except Exception as e:
        printError('Error: failed to read the configuration from %s' % config_file)
    return config


########################################
##### Tests
########################################

#
# Pass all conditions?
#
def pass_conditions(conditions, obj, all_info, current_path, current_value):
    if not conditions:
        return True
    test_path = copy.deepcopy(current_path)
    test_path.append(current_value)
    for condition in conditions:
        key, test, value = condition
        target_obj = all_info
        for p in test_path:
            target_obj = target_obj[p]
        target_obj = get_values_at(target_obj, {}, key.split('.'))
        if type(target_obj) == list:
            one_match = False
            for v in target_obj:
                if pass_condition(test, value, v):
                    one_match = True
            if not one_match:
                return False
        else:
            res = pass_condition(test, value, target_obj)
            if not res:
                return False
    return True

#
# Generic tests
#
def pass_condition(test, a, b):
    if test == 'contain':
        return b in a
    elif test == 'equal':
        return a == b
    elif test == 'notEqual':
        return a != b
    elif test == 'empty':
        return ((type(b) == dict and b == {}) or (type(b) == list and b == []))
    elif test == 'notEmpty':
        return not ((type(b) == dict and b == {}) or (type(b) == list and b == []))
    elif test == 'match':
        return re.match(a, b) != None
    elif test == 'notMatch':
        return re.match(a, b) == None
    elif test == 'null':
        return b == None
    elif test == 'notNull':
        return b != None
    elif test == 'dateOlderThan':
        try:
            age = (datetime.datetime.today() - dateutil.parser.parse(b).replace(tzinfo=None)).days
            return age > a
        except Exception as e:
            # Failure means an invalid date, meaning no activity
            return True
    return False


########################################
##### Get values
########################################

#
# Get key at... there's probably a way to clean that ??
#
def macro_get_key_at(all_info, info, current_path, key, value, k):
    if k == 'this':
        result = value
    else:
        path_to_key = k.split('.')
        first = path_to_key[0]
        last = path_to_key[-1]
        if first in supported_services:
            # TODO: is this broken?
            print(first)
        elif last in current_path:
            index_of_key = current_path.index(last) + 1
            result = current_path[index_of_key]
        else:
            tmp = copy.deepcopy(current_path)
            tmp.append(value)
            tmp = tmp + path_to_key
            result = get_values_at(all_info, {}, tmp)
    return result

#
# Get arbitrary object given a dictionary and path (list of keys)
#
def get_values_at(dictionary, dic, path):
    values = []
    if not dic:
        dic = dictionary
    for p in path:
        if type(dic) == dict and p in dic:
            dic = dic[p]
            if p == path[-1]:
                values.append(dic)
        elif type(dic) == list:
            for entry in dic:
                test = path[path.index(p):]
                values = values + get_values_at(dictionary, entry, test)
    return values


########################################
##### Recursion
########################################

#
# Meat and potato is here...
#
def list_all(all_info, info, path, current_path, keys, conditions):
    key = path.pop(0)
    if key in info:
        current_path.append(key)
        for value in info[key]:
            if len(path) == 0:
                if type(info[key]) == dict:
                    # Check that all conditions are met
                    if pass_conditions(conditions, info[key][value], all_info, current_path, value):
                        # TODO: allow for other formatting than CSV and clean that code
                        output = ''
                        for k in keys:
                            key_value = macro_get_key_at(all_info, info, current_path, key, value, k)
                            key_value = key_value[0] if (type(key_value) == list and len(key_value) == 1) else key_value
                            if output:
                                output = output + ', ' + str(key_value)
                            else:
                                output = str(key_value)
                        printInfo(output)
                else:
                    raise Exception
            else:
                # keep track of where we are...
                tmp = copy.deepcopy(current_path)
                tmp.append(value)
                list_all(all_info, info[key][value], copy.deepcopy(path), tmp, keys, conditions)


########################################
##### Main
########################################

def main(cmd_args):

    # Configure the debug level
    configPrintException(cmd_args.debug)

    # Get the environment name
    if len(cmd_args.environment_names) < 1:
        printError('Error: you need to specify an environment name.')
        return 42

    # Load arguments from config if specified
    if len(cmd_args.config):
        config = read_dump_config(cmd_args.config[0])
        if config:
            args = Bunch(config)
        else:
            return 42
    else:
        args = cmd_args

    # Conditions are optional
    conditions = args.conditions if hasattr(args, 'conditions') else None

    # Support multiple environments
    for environment_name in cmd_args.environment_names:

        # Load the data
        aws_config = {}
        for service in supported_services:
            try:
                aws_config[service] = load_info_from_json(service, environment_name)
            except Exception as e:
                printException(e)

        # Output stuff
        for entity in args.entities:
            entity = entity.split('.')
            service = entity.pop(0)
            list_all(aws_config, aws_config[service], entity, [ service ], args.keys, conditions)


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

parser.add_argument('--config',
                    dest='config',
                    default=[],
                    nargs='+',
                    help='Config file that sets the entities and keys to be listed.')
parser.add_argument('--env',
                    dest='environment_names',
                    default=[],
                    nargs='+',
                    help='AWS environment name (used to create multiple reports)')
parser.add_argument('--entities',
                    dest='entities',
                    default=[],
                    nargs='+',
                    help='Path of the entities to list (e.g. iam.users or ec2.regions.vpcs)')
parser.add_argument('--keys',
                    dest='keys',
                    default=[],
                    nargs='+',
                    help='Keys to be printed for the given object.')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
