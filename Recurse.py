#!/usr/bin/env python

# Import AWS Scout2 tools
from AWSScout2.utils import *

# Import third-party packages
import datetime
import dateutil.parser
import netaddr
import re
import sys

re_profile = re.compile(r'.*?_PROFILE_.*?')
re_ip_ranges_from_file = re.compile(r'_IP_RANGES_FROM_FILE_\((.*?),\s*(.*?)\)')
aws_ip_ranges = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'

########################################
##### Config file
########################################

class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)

#
# Read arguments from a config file
#
def read_dump_config(config_file, environment_name, ip_ranges):
    config = None
    try:
        with open(config_file, 'rt') as f:
            config = json.load(f)
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
    except Exception as e:
        printException(e)
        printError('Error: failed to read the configuration from %s' % config_file)
    return config    


########################################
##### Tests
########################################

def get_value_at(all_info, current_path, key):
    keys = key.split('.')
    if keys[-1] == 'id':
        target_obj = current_path[len(keys)-1]
    else:
        if key == 'this':
            target_path = current_path
        elif '.' in key:
            target_path = current_path[0:len(keys)-1]
            if keys[-1] != 'id' and keys[-1] != '':
                target_path.append(keys[-1])
        else:
            target_path = copy.deepcopy(current_path)
            target_path.append(key)
        target_obj = all_info
        for p in target_path:
            # Handle lists...
            if type(target_obj) == list and p == current_path[-1]:
                target_obj = p
            else:
                target_obj = target_obj[p]
    return str(target_obj)

#
# Pass all conditions?
#
def pass_conditions(all_info, current_path, conditions):
    for condition in conditions:
        # Conditions are formed as "path to value", "type of test", "value(s) for test"
        path_to_value, test_name, test_values = condition
        target_obj = get_value_at(all_info, current_path, path_to_value)
        res = pass_condition(target_obj, test_name, test_values)
        if not res:
            return False
    return True



########################################
##### Recursion
########################################

def recurse(all_info, current_info, target_path, current_path, config):
    if len(target_path) == 0:
        if pass_conditions(all_info, current_path, config['conditions']):
            # Will need to pass a mode
            if False:
                pass
            elif True:
                # Print mode
                output = ''
                for key in config['listing']['keys']:
                    if not output:
                        output = get_value_at(all_info, current_path, key)
                    else:
                        output = output + ', ' + get_value_at(all_info, current_path, key)
                print output
        return
    target_path = copy.deepcopy(target_path)
    current_path = copy.deepcopy(current_path)
    attribute = target_path.pop(0)
    if type(current_info) == dict:
        if attribute in current_info:
            split_path = copy.deepcopy(current_path)
            split_path.append(attribute)
            recurse(all_info, current_info[attribute], target_path, split_path, config)
        elif attribute == 'id':
            for key in current_info:
                split_target_path = copy.deepcopy(target_path)
                split_current_path = copy.deepcopy(current_path)
                split_current_path.append(key)
                split_current_info = current_info[key]
                recurse(all_info, split_current_info, split_target_path, split_current_path, config)
    # To handle lists properly, I would have to make sure the list is properly ordered and I can use the index to consistently access an object... Investigate (or do not use lists)
    elif type(current_info) == list:
        for split_current_info in current_info:
            split_path = copy.deepcopy(current_path)
            split_path.append(split_current_info)
            recurse(all_info, split_current_info, copy.deepcopy(target_path), split_path, config)
    else:
        printError('Error: unhandled case, typeof(current_info) = %s' % type(current_info))
        printError(current_info)


########################################
##### Main
########################################

def main(cmd_args):

    # Configure the debug level
    configPrintException(cmd_args.debug)

    # Get the environment name
    environment_names = get_environment_name(cmd_args)

    # Support multiple environments
    for environment_name in environment_names:

        # Load arguments from config if specified
        if len(cmd_args.config):
            config = read_dump_config(cmd_args.config[0], environment_name, cmd_args.ip_ranges)
            if config:
                args = Bunch(config)
            else:
                return 42
        else:
            args = cmd_args

        # Conditions and mapping are optional
        conditions = args.conditions if hasattr(args, 'conditions') else None
        mapping = args.mapping if hasattr(args, 'mapping') else []

        # Load the data
        aws_config = {}
        aws_config['services'] = {}
        for service in supported_services:
            try:
                aws_config['services'][service] = load_info_from_json(service, environment_name)
            except Exception as e:
                printException(e)

        # Output stuff (this loop should be reviewed)
        for entity in args.entities:
            target_path = entity.split('.')
            current_path = []
            recurse(aws_config['services'], aws_config['services'], target_path, current_path, config) #, [ service ], args.keys, conditions, output_format, mapping)

#            service = entity.pop(0)
#            if output_format != 'csv':
#                printInfo(output_format['header'])
#            list_all(aws_config, aws_config[service], entity, [ service ], args.keys, conditions, output_format, mapping)
#            if output_format != 'csv':
#                printInfo(output_format['footer'])


########################################
##### Argument parser
########################################

default_args = read_profile_default_args(parser.prog)

add_scout2_argument(parser, default_args, 'env')

parser.add_argument('--config',
                    dest='config',
                    default=[],
                    nargs='+',
                    help='Config file that sets the entities and keys to be listed.')
parser.add_argument('--format',
                    dest='format',
                    default=['csv'],
                    nargs='+',
                    help='Bleh.')
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
parser.add_argument('--ip-ranges',
                    dest='ip_ranges',
                    default=[],
                    nargs='+',
                    help='Config file(s) that contain your own IP ranges.')

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
