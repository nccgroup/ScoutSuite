# Import future print
from __future__ import print_function

# Import opinel
from opinel.utils import *

# Import stock packages
import argparse
import datetime
from distutils import dir_util
import copy
import json
import glob
import os
import re
import shutil
import sys
import traceback

# Python2 vs Python3
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

# Import third-party packages
import requests

########################################
# Globals
########################################

supported_services = []
re_service_utils = re.compile(r'^utils_(.*?).py$')
scout2_utils_dir, foo = os.path.split(__file__)
for filename in os.listdir(scout2_utils_dir):
    service = re_service_utils.match(filename)
    if service: # and service.groups()[0] != 'vpc':
        supported_services.append(service.groups()[0])

ec2_classic = 'EC2-Classic'
condition_operators = [ 'and', 'or' ]


#re_profile = re.compile(r'.*?_PROFILE_.*?')
re_ip_ranges_from_file = re.compile(r'_IP_RANGES_FROM_FILE_\((.*?),\s*(.*?)\)')
re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')
aws_ip_ranges = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'

########################################
##### Argument parser
########################################

#
# Add a shared argument to a Scout2 utility
#
def add_scout2_argument(parser, default_args, argument_name):
    if argument_name == 'force':
        parser.add_argument('--force',
                            dest='force_write',
                            default=False,
                            action='store_true',
                            help='Overwrite existing json files')
    elif argument_name == 'ruleset-name':
        parser.add_argument('--ruleset-name',
                            dest='ruleset_name',
                            default=['default'],
                            nargs='+',
                            help='Customized set of rules')
    elif argument_name == 'services':
        parser.add_argument('--services',
                            dest='services',
                            default=supported_services,
                            nargs='+',
                            help='Name of the Amazon Web Services you want to work with')
    elif argument_name == 'skip':
        parser.add_argument('--skip',
                            dest='skipped_services',
                            default=[],
                            nargs='+',
                            help='Name of services you want to ignore')
    elif argument_name == 'env':
        parser.add_argument('--env',
                            dest='environment_name',
                            default=[],
                            nargs='+',
                            help='AWS environment name (used when working with multiple reports)')
    else:
        raise Exception('Invalid parameter name %s' % argument_name)


########################################
# Common functions
########################################

#
# Return the list of services to iterate over
#
def build_services_list(services = supported_services, skipped_services = []):
    enabled_services = []
    for s in services:
        if s in supported_services and s not in skipped_services:
            enabled_services.append(s)
    return enabled_services

#
# Return attribute value at a given path
#
def get_attribute_at(config, target_path, key, default_value = None):
    for target in target_path:
        config = config[target]
    return config[key] if key in config else default_value

#
# Get arbitrary object given a dictionary and path (list of keys)
#
def get_object_at(dictionary, path, attribute_name = None):
    o = dictionary
    for p in path:
        o = o[p]
    if attribute_name:
        return o[attribute_name]
    else:
        return o

#
# Recursively go to a target and execute a callback
#
def go_to_and_do(aws_config, current_config, path, current_path, callback, callback_args):
    key = path.pop(0)
    if not current_config:
        current_config = aws_config
    if not current_path:
        current_path = []
    if key in current_config:
        current_path.append(key)
        for value in current_config[key]:
            if len(path) == 0:
                if type(current_config[key] == dict) and type(value) != dict and type(value) != list:
                    callback(aws_config, current_config[key][value], path, current_path, value, callback_args)
                else:
                    # TODO: the current_config value passed here is not correct...
                    callback(aws_config, current_config, path, current_path, value, callback_args)
            else:
                # keep track of where we are...
                tmp = copy.deepcopy(current_path)
                tmp.append(value)
                go_to_and_do(aws_config, current_config[key][value], copy.deepcopy(path), tmp, callback, callback_args)

#
# JSON encoder class
#
class Scout2Encoder(json.JSONEncoder):
    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return o.__dict__

#
# Copies the value of keys from source object to dest object
#
def get_keys(src, dst, keys):
    for key in keys:
        dst[no_camel(key)] = src[key] if key in src else None

#
# Converts CamelCase to camel_case
#
def no_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()                                                                                                                                 


########################################
# Violations search functions
########################################

def has_instances(ec2_region):
    count = 0
    for v in ec2_region['vpcs']:
        if 'instances' in ec2_region['vpcs'][v]:
            count = count + len(ec2_region['vpcs'][v]['instances'])
    return False if count == 0 else True

def match_instances_and_roles(ec2_config, iam_config):
    role_instances = {}
    for r in ec2_config['regions']:
        for v in ec2_config['regions'][r]['vpcs']:
            if 'instances' in ec2_config['regions'][r]['vpcs'][v]:
                for i in ec2_config['regions'][r]['vpcs'][v]['instances']:
                    instance_profile_id = ec2_config['regions'][r]['vpcs'][v]['instances'][i]['iam_instance_profile']['id'] if 'iam_instance_profile' in ec2_config['regions'][r]['vpcs'][v]['instances'][i] else None
                    if instance_profile_id:
                        manage_dictionary(role_instances, instance_profile_id, [])
                        role_instances[instance_profile_id].append(i)
    for role_id in iam_config['roles']:
        iam_config['roles'][role_id]['instances_count'] = 0
        for instance_profile_id in iam_config['roles'][role_id]['instance_profiles']:
            if instance_profile_id in role_instances:
                iam_config['roles'][role_id]['instance_profiles'][instance_profile_id]['instances'] = role_instances[instance_profile_id]
                iam_config['roles'][role_id]['instances_count'] += len(role_instances[instance_profile_id])


#
# Create dashboard metadata
#
def create_report_metadata(aws_config, services):
    # Load resources and summaries metadata from file
    with open('dropdown.json', 'rt') as f:
        aws_config['old_metadata'] = json.load(f)
    with open('metadata.json', 'rt') as f:
        aws_config['metadata'] = json.load(f)    
    for service in aws_config['metadata']:
        for resource in aws_config['metadata'][service]['resources']:
            # full_path = path if needed
            if not 'full_path' in aws_config['metadata'][service]['resources'][resource]:
                aws_config['metadata'][service]['resources'][resource]['full_path'] = aws_config['metadata'][service]['resources'][resource]['path']
            # Script is the full path minus "id" (TODO: change that)
            if not 'script' in aws_config['metadata'][service]['resources'][resource]:
                aws_config['metadata'][service]['resources'][resource]['script'] = '.'.join([x for x in aws_config['metadata'][service]['resources'][resource]['full_path'].split('.') if x != 'id'])
            # Update counts here
#            config = {'conditions': []}
#            recurse(aws_config, aws_config, aws_config['metadata'][service]['resources'][resource]['full_path'].split('.'), [], config)


########################################
##### Recursion
########################################

def recurse(all_info, current_info, target_path, current_path, config, add_suffix = False):
    results = []
    if len(target_path) == 0:
        # Dashboard: count the number of processed entities here
        manage_dictionary(config, 'checked_items', 0)
        config['checked_items'] = config['checked_items'] + 1
        # Test for conditions...
        if pass_conditions(all_info, current_path, copy.deepcopy(config['conditions'])):
            if add_suffix and 'id_suffix' in config:
                current_path.append(config['id_suffix'])
            results.append('.'.join(current_path))
        # Return the flagged items...
        config['flagged_items'] = len(results)
        return results
            # 
            # Will need to pass a mode
#            if False:
#                pass
#            elif True:
#                # Print mode
#                output = ''
#                for key in config['listing']['keys']:
#                    if not output:
#                        output = get_value_at(all_info, current_path, key, True)
#                    else:
#                        output = output + ', ' + get_value_at(all_info, current_path, key, True)
#                print output

    target_path = copy.deepcopy(target_path)
    current_path = copy.deepcopy(current_path)
    attribute = target_path.pop(0)
    if type(current_info) == dict:
        if attribute in current_info:
            split_path = copy.deepcopy(current_path)
            split_path.append(attribute)
            results = results + recurse(all_info, current_info[attribute], target_path, split_path, config, add_suffix)
        elif attribute == 'id':
            for key in current_info:
                split_target_path = copy.deepcopy(target_path)
                split_current_path = copy.deepcopy(current_path)
                split_current_path.append(key)
                split_current_info = current_info[key]
                results = results + recurse(all_info, split_current_info, split_target_path, split_current_path, config, add_suffix)
    # To handle lists properly, I would have to make sure the list is properly ordered and I can use the index to consistently access an object... Investigate (or do not use lists)
    elif type(current_info) == list:
        for index, split_current_info in enumerate(current_info):
            split_current_path = copy.deepcopy(current_path)
            split_current_path.append(str(index))
            results = results + recurse(all_info, split_current_info, copy.deepcopy(target_path), split_current_path, config, add_suffix)
    else:
        printError('Error: unhandled case, typeof(current_info) = %s' % type(current_info))
        printError(current_info)
    return results


#
# Pass all conditions?
#
def pass_conditions(all_info, current_path, conditions):
    result = False
    if len(conditions) == 0:
        return True
    condition_operator = conditions.pop(0)
    for condition in conditions:
      if condition[0] in condition_operators:
        res = pass_conditions(all_info, current_path, condition)
      else:
        # Conditions are formed as "path to value", "type of test", "value(s) for test"
        path_to_value, test_name, test_values = condition
        target_obj = get_value_at(all_info, current_path, path_to_value)
        if type(test_values) != list:
            dynamic_value = re_get_value_at.match(test_values)
            if dynamic_value:
                test_values = get_value_at(all_info, current_path, dynamic_value.groups()[0], True)
        res = pass_condition(target_obj, test_name, test_values)
      # Quick exit and + false
      if condition_operator == 'and' and not res:
          return False
      # Quick exit or + true
      if condition_operator == 'or' and res:
          return True
    # Still here ?
    # or -> false
    # and -> true
    if condition_operator == 'or':
        return False
    else:
        return True

#
# Get value located at a given path
#
def get_value_at(all_info, current_path, key, to_string = False):
    keys = key.split('.')
    if keys[-1] == 'id':
        target_obj = current_path[len(keys)-1]
    else:
        if key == 'this':
            target_path = current_path
        elif '.' in key:
            target_path = []
            for i, key in enumerate(keys):
                if key == 'id':
                    target_path.append(current_path[i])
                else:
                    target_path.append(key)
            if len(keys) > len(current_path):
                target_path = target_path + keys[len(target_path):]
        else:
            target_path = copy.deepcopy(current_path)
            target_path.append(key)
        target_obj = all_info
        for p in target_path:
          try:
            if type(target_obj) == list and type(target_obj[0]) == dict:
                target_obj = target_obj[int(p)]                
            elif type(target_obj) == list:
                target_obj = p
            elif p == '':
                target_obj = target_obj
            else:
              try:
                target_obj = target_obj[p]
              except Exception as e:
                print(target_obj)
                printException(e)
                raise Exception
          except Exception as e:
            print(target_obj)
            printException(e)
            raise Exception
    if to_string:
        return str(target_obj)
    else:
        return target_obj


########################################
# File read/write functions
########################################

AWSCONFIG_DIR = 'inc-awsconfig'
AWSCONFIG_FILE = 'aws_config.js'
REPORT_TITLE  = 'AWS Scout2 Report'

def create_scout_report(environment_name, aws_config, force_write, debug):
    # Save data
    save_config_to_file(environment_name, aws_config, force_write, debug)
    # Create the HTML report using all partials under html/partials/
    contents = ''
    for filename in glob.glob('html/partials/*'):
        with open('%s' % filename, 'rt') as f:
            contents = contents + f.read()
    # Use all scripts under html/summaries/
    for filename in glob.glob('html/summaries/*'):
        with open('%s' % filename, 'rt') as f:
            contents = contents + f.read()
    services = [service for service in aws_config['services']]
    services.append('global')
    for service in services: # aws_config['services']:
        if os.path.exists('html/%s.html' % service):
            with open('html/%s.html' % service, 'rt') as f:
                contents = contents + f.read()
    if environment_name != 'default':
        def_report_filename, def_config_filename = get_scout2_paths('default')
        new_report_filename, new_config_filename = get_scout2_paths(environment_name)
        new_file = 'report-' + environment_name + '.html'
    else:
        new_file = 'report.html'
    printInfo('Creating %s ...' % new_file)
    if prompt_4_overwrite(new_file, force_write):
        if os.path.exists(new_file):
            os.remove(new_file)
        with open('html/report.html') as f:
            with open(new_file, 'wt') as nf:
                for line in f:
                    newline = line.replace(REPORT_TITLE, REPORT_TITLE + ' [' + environment_name + ']')
                    newline = newline.replace(def_config_filename, new_config_filename)
                    newline = newline.replace('<!-- PLACEHOLDER -->', contents)
                    nf.write(newline)

#
# Return the filename of the Scout2 report and config
#
def get_scout2_paths(environment_name):
    if environment_name == 'default':
        report_filename = 'report.html'
        config_filename = AWSCONFIG_DIR + '/' + AWSCONFIG_FILE
    else:
        report_filename = ('report-%s.html' % environment_name)
        config_filename = ('%s-%s/%s' % (AWSCONFIG_DIR, environment_name, AWSCONFIG_FILE))
    return report_filename, config_filename

def load_info_from_json(service, environment_name):
    report_filename, config_filename = get_scout2_paths(environment_name)
    try:
        if os.path.isfile(config_filename):
            with open(config_filename) as f:
                json_payload = f.readlines()
                json_payload.pop(0)
                json_payload = ''.join(json_payload)
                aws_config = json.loads(json_payload)
        else:
            aws_config = {}
    except Exception as e:
        printException(e)
        return {}
    return aws_config['services'][service] if 'services' in aws_config and service in aws_config['services'] else {}

def load_from_json(environment_name, var):
    report_filename, config_filename = get_scout2_paths(environment_name)
    with open(report_filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)

#
# Load rule from a JSON config file
#
def load_config_from_json(rule_metadata, environment_name, ip_ranges):
    config = None
    config_file = 'rules/%s' % rule_metadata['filename']
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
            if c1 in condition_operators:
                continue
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
        # Fix level if specified in ruleset
        if 'level' in rule_metadata:
            rule['level'] = rule_metadata['level']
    except Exception as e:
        printException(e)
        printError('Error: failed to read the rule from %s' % config_file)
    return config

def open_file(environment_name, force_write):
    printInfo('Saving AWS config...')
    report_filename, config_filename = get_scout2_paths(environment_name)
    if prompt_4_overwrite(config_filename, force_write):
       try:
           config_dirname = os.path.dirname(config_filename)
           if not os.path.isdir(config_dirname):
               os.makedirs(config_dirname)
           return open(config_filename, 'wt')
       except Exception as e:
           printException(e)
    else:
        return None

def prompt_4_yes_no(question):
    while True:
        sys.stdout.write(question + ' (y/n)? ')
        try:
            choice = raw_input().lower()
        except:
            choice = input().lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            printError('\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice)

def prompt_4_overwrite(filename, force_write):
    # Do not prompt if the file does not exist or force_write is set
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_4_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename))

def save_blob_to_file(filename, blob, force_write, debug):
    try:
        if prompt_4_overwrite(filename, force_write):
            with open(filename, 'wt') as f:
                write_data_to_file(f, blob, force_write, debug)
    except Exception as e:
        printException(e)
        pass

#
# Save AWS configuration (python dictionary) as JSON
#
def save_config_to_file(environment_name, aws_config, force_write, debug):
    try:
        with open_file(environment_name, force_write) as f:
            print('aws_info =', file = f)
            write_data_to_file(f, aws_config, force_write, debug)
    except Exception as e:
        printException(e)
        pass

def write_data_to_file(f, aws_config, force_write, debug):
    print('%s' % json.dumps(aws_config, indent = 4 if debug else None, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder), file = f)


########################################
# Status update functions
########################################

def init_status(items, keyword=None, fetched=0):
    count = fetched
    total = 0
    if items:
        total = len(items)
    update_status(0, total, keyword)
    return count, total

def update_status(current, total, keyword=None):
    if keyword:
        keyword = keyword + ':'
    else:
        keyword = ''
    if total != 0:
        sys.stdout.write("\r%s %d/%d" % (keyword , current, total))
    else:
        sys.stdout.write("\r%s %d" % (keyword, current))
    sys.stdout.flush()
    return current + 1

def close_status(current, total, keyword=None):
    update_status(current, total, keyword)
    sys.stdout.write('\n')
