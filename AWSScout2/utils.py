# -*- coding: utf-8 -*-

# Import future stuff...
from __future__ import print_function
from __future__ import unicode_literals

# Import opinel
from opinel.utils import *
from AWSScout2.rules import condition_operators

# Import stock packages
import datetime
import copy
import json
import hashlib
import os
import re
import sys

# Python2 vs Python3
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2


########################################
# Globals
########################################

re_ip_ranges_from_file = re.compile(r'_IP_RANGES_FROM_FILE_\((.*?),\s*(.*?)\)')
re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')
re_list_value = re.compile(r'_LIST_\((.*?)\)')
aws_ip_ranges_filename = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'

ec2_classic = 'EC2-Classic'

formatted_service_name = {
    'cloudtrail': 'CloudTrail',
    'cloudwatch': 'CloudWatch',
    'lambda': 'Lambda',
    'redshift': 'RedShift',
    'route53': 'Route53'
}


########################################
# Functions
########################################


def format_service_name(service):
    """

    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()


def get_attribute_at(config, target_path, key, default_value = None):
    """
    Return attribute value at a given path

    :param config:
    :param target_path:
    :param key:
    :param default_value:
    :return:
    """
    for target in target_path:
        config = config[target]
    return config[key] if key in config else default_value


def get_object_at(dictionary, path, attribute_name = None):
    """
    Get arbitrary object given a dictionary and path (list of keys)

    :param dictionary:
    :param path:
    :param attribute_name:
    :return:
    """
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


def get_keys(src, dst, keys):
    """
    Copies the value of keys from source object to dest object

    :param src:
    :param dst:
    :param keys:
    :return:
    """
    for key in keys:
        dst[no_camel(key)] = src[key] if key in src else None


def no_camel(name):
    """
    Converts CamelCase to camel_case

    :param name:
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()                                                                                                                                 


def recurse(all_info, current_info, target_path, current_path, config, add_suffix = False):
    """

    :param all_info:
    :param current_info:
    :param target_path:
    :param current_path:
    :param config:
    :param add_suffix:
    :return:
    """
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


def pass_conditions(all_info, current_path, conditions):
    """
    Pass all conditions?

    :param all_info:
    :param current_path:
    :param conditions:
    :return:
    """
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


def get_value_at(all_info, current_path, key, to_string = False):
    """
    Get value located at a given path

    :param all_info:
    :param current_path:
    :param key:
    :param to_string:
    :return:
    """
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


def get_non_aws_id(name):
    """
    Not all AWS resources have an ID, use SHA1(name) when the resource name is used

    :param name:
    :return:
    """
    m = hashlib.sha1()
    m.update(name.encode('utf-8'))
    return m.hexdigest()


def format_listall_output(format_file, format_item_dir, format, config, option_prefix = None, template = None, skip_options = False):
    """
    Prepare listall output template

    :param format_file:
    :param format_item_dir:
    :param format:
    :param config:
    :param option_prefix:
    :param template:
    :param skip_options:
    :return:
    """
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


def generate_listall_output(lines, resources, aws_config, template, arguments, nodup = False):
    """
    Format and print the output of ListAll

    :param lines:
    :param resources:
    :param aws_config:
    :param template:
    :param arguments:
    :param nodup:
    :return:
    """
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
    """
    Ask a question and prompt for yes or no

    :param question:                    Question to ask; answer is yes/no
    :return:                            :boolean
    """
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
    """
    Confirm before overwriting existing files. Do not prompt if the file does not exist or force_write is set

    :param filename:                    Name of the file to be overwritten
    :param force_write:                 Do not ask for confirmation and automatically return True if set
    :return:                            :boolean
    """
    #
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_4_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename))
