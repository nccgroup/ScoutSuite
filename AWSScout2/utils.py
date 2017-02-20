# -*- coding: utf-8 -*-

# Import future stuff...
from __future__ import print_function
from __future__ import unicode_literals

# Import opinel
from opinel.utils import *

# Import stock packages
import argparse
import botocore
import datetime
from distutils import dir_util
import copy
import json
import glob
import hashlib
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


########################################
# Globals
########################################

supported_services = []
re_service_utils = re.compile(r'^utils_(.*?).py$')
scout2_utils_dir, foo = os.path.split(__file__)
for filename in os.listdir(scout2_utils_dir):
    service = re_service_utils.match(filename)
    if service and service.groups()[0] != 'vpc':
        supported_services.append(service.groups()[0])

ec2_classic = 'EC2-Classic'
condition_operators = [ 'and', 'or' ]


re_ip_ranges_from_file = re.compile(r'_IP_RANGES_FROM_FILE_\((.*?),\s*(.*?)\)')
re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')
re_list_value = re.compile(r'_LIST_\((.*?)\)')
aws_ip_ranges_filename = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'

FILTERS_DIR = 'filters'
RULES_DIR = 'rules'
RULESETS_DIR = 'rulesets'
DEFAULT_RULESET = '%s/default.json' % RULESETS_DIR


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
    elif argument_name == 'ruleset':
        parser.add_argument('--ruleset',
                            dest='ruleset',
                            default=[ DEFAULT_RULESET ],
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
    elif argument_name == 'scout2-path':
        parser.add_argument('--scout2-path',
                            dest='scout2_path',
                            default=None,
                            nargs='+',
                            help='Path to Scout2 tool')
    elif argument_name == 'format':
        parser.add_argument('--format',
                            dest='format',
                            default=['csv'],
                            nargs='+',
                            help='Listall output format')
    elif argument_name == 'format-file':
        parser.add_argument('--format-file',
                            dest='format_file',
                            default=None,
                            nargs='+',
                            help='Listall output format file')
    else:
        raise Exception('Invalid parameter name %s' % argument_name)


########################################
# Common functions
########################################



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
# JSON encoder class
#
class Scout2Encoder(json.JSONEncoder):
    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return vars(o)

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



########################################
##### Recursion
########################################

def recurse(all_info, current_info, target_path, current_path, config, add_suffix = False):
    results = []
    if len(target_path) == 0:
        # Dashboard: count the number of processed resources here
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
        printError(str(current_info))
        raise Exception
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
                printError('Current path: %s' % str(current_path))
                #print(target_obj)
                printException(e)
                raise Exception
          except Exception as e:
            printError('Current path: %s' % str(current_path))
            #print(target_obj)
            printException(e)
            raise Exception
    if to_string:
        return str(target_obj)
    else:
        return target_obj

#
# Not all AWS resources have an ID
# Use SHA1(name) when the resource name is used
#
def get_non_aws_id(name):
    m = hashlib.sha1()
    m.update(name.encode('utf-8'))
    return m.hexdigest()


########################################
# File read/write functions
########################################

AWSCONFIG_DIR = 'inc-awsconfig'
AWSCONFIG_FILE = 'aws_config'
AWSRULESET_FILE = 'aws_ruleset'
REPORT_TITLE  = 'AWS Scout2 Report'

def create_scout_report(environment_name, timestamp, aws_config, exceptions, force_write, debug):
    if timestamp:
        environment_name = '%s-%s' % (environment_name, timestamp)
    # Fix bug mentioned in #111
    environment_name = environment_name.replace('/', '_').replace('\\', '_')
    # Save data
    save_config_to_file(environment_name, aws_config, force_write, debug)
    save_config_to_file(environment_name, exceptions, force_write, debug, js_filename = 'exceptions', js_varname = 'exceptions')
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
        foo, def_exceptions_filename = get_scout2_paths('default', js_filename = 'exceptions')
        new_report_filename, new_config_filename = get_scout2_paths(environment_name)
        foo, new_exceptions_filename = get_scout2_paths(environment_name, js_filename = 'exceptions')
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
                    if environment_name != 'default':
                        newline = newline.replace(def_config_filename, new_config_filename)
                        newline = newline.replace(def_exceptions_filename, new_exceptions_filename)
                    newline = newline.replace('<!-- PLACEHOLDER -->', contents)
                    nf.write(newline)

#
# Return the filename of the Scout2 report and config
#
def get_scout2_paths(environment_name, scout2_folder = None, js_filename = None):
    if not js_filename:
        js_filename = AWSCONFIG_FILE
    if environment_name == 'default':
        report_filename = 'report.html'
        config_filename = AWSCONFIG_DIR + '/' + js_filename + '.js'
    else:
        report_filename = ('report-%s.html' % environment_name)
        config_filename = ('%s/%s-%s.js' % (AWSCONFIG_DIR, js_filename, environment_name))
    if scout2_folder:
        report_filename = os.path.join(scout2_folder[0], report_filename)
        config_filename = os.path.join(scout2_folder[0], config_filename)
    return report_filename, config_filename

#
# Prepare listall output template
#
def format_listall_output(format_file, format_item_dir, format, config, option_prefix = None, template = None, skip_options = False):
        # Set the list of keys if printing from a file spec
        # _LINE_(whatever)_EOL_
        # _ITEM_(resource)_METI_
        # _KEY_(path_to_value)
        if format_file and os.path.isfile(format_file):
            if not template:
                with open(format_file, 'rt') as f:
                    template = f.read()
            # Optional files
            if not skip_options:
                re_option = re.compile(r'(%_OPTION_\((.*?)\)_NOITPO_)')
                optional_files = re_option.findall(template)
                for optional_file in optional_files:
                    if optional_file[1].startswith(option_prefix + '-'):
                        with open(os.path.join(format_item_dir, optional_file[1].strip()), 'rt') as f:
                            template = template.replace(optional_file[0].strip(), f.read())
            # Include files if needed
            re_file = re.compile(r'(_FILE_\((.*?)\)_ELIF_)')
            while True:
                requested_files = re_file.findall(template)
                available_files = os.listdir(format_item_dir)
                for requested_file in requested_files:
                    if requested_file[1].strip() in available_files:
                        with open(os.path.join(format_item_dir, requested_file[1].strip()), 'rt') as f:
                            template = template.replace(requested_file[0].strip(), f.read())
                # Find items and keys to be printed
                re_line = re.compile(r'(_ITEM_\((.*?)\)_METI_)')
                re_key = re.compile(r'_KEY_\(*(.*?)\)', re.DOTALL|re.MULTILINE) # Remove the multiline ?
                format_item_mappings = os.listdir(format_item_dir)
                lines = re_line.findall(template)
                for (i, line) in enumerate(lines):
                    lines[i] = line + (re_key.findall(line[1]),)
                requested_files = re_file.findall(template)
                if len(requested_files) == 0:
                    break
        elif format and format[0] == 'csv':
            keys = config['keys']
            line = ', '.join('_KEY_(%s)' % k for k in keys)
            lines = [ (line, line, keys) ]
            template = line
        return (lines, template)

def load_info_from_json(service, environment_name, scout2_folder = None, full_config = False):
    report_filename, config_filename = get_scout2_paths(environment_name, scout2_folder = scout2_folder)
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
    if full_config:
        return aws_config
    else:
        return aws_config['services'][service] if 'services' in aws_config and service in aws_config['services'] else {}

def load_from_json(environment_name, config_filename = None):
    if not config_filename:
        report_filename, config_filename = get_scout2_paths(environment_name)
    with open(config_filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)


def open_file(environment_name, force_write, js_filename, quiet = False):
    if not quiet:
        printInfo('Saving config...')
    report_filename, config_filename = get_scout2_paths(environment_name, js_filename = js_filename)
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

#
# Format and print the output of ListAll 
#
def generate_listall_output(lines, resources, aws_config, template, arguments, nodup = False):
    for line in lines:
        output = []
        for resource in resources:
            current_path = resource.split('.')
            outline = line[1]
            for key in line[2]:
                outline = outline.replace('_KEY_('+key+')', get_value_at(aws_config['services'], current_path, key, True))
            output.append(outline)
        output = '\n'.join(line for line in sorted(set(output)))
        template = template.replace(line[0], output)
    for (i, argument) in enumerate(arguments):
        template = template.replace('_ARG_%d_' % i, argument)
    return template

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
def save_config_to_file(environment_name, config, force_write = False, debug = False, js_filename = AWSCONFIG_FILE, js_varname = 'aws_info', quiet = False):
    try:
        with open_file(environment_name, force_write, js_filename, quiet) as f:
            print('%s =' % js_varname, file = f)
            write_data_to_file(f, config, force_write, debug)
    except Exception as e:
        printException(e)
        pass

def write_data_to_file(f, aws_config, force_write, debug):
    print('%s' % json.dumps(aws_config, indent = 4 if debug else None, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder), file = f)

