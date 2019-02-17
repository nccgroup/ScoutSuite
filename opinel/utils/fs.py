# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import json
import os
import yaml

from opinel.utils.console import printError, printException, prompt_4_overwrite
from opinel.utils.conditions import pass_condition



class CustomJSONEncoder(json.JSONEncoder):
    """
    JSON encoder class
    """
    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return o.__dict__


def load_data(data_file, key_name = None, local_file = False, format = 'json'):
    """
    Load a JSON data file

    :param data_file:
    :param key_name:
    :param local_file:
    :return:
    """
    if local_file:
        if data_file.startswith('/'):
            src_file = data_file
        else:
            src_dir = os.getcwd()
            src_file = os.path.join(src_dir, data_file)
    else:
        src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        if not os.path.isdir(src_dir):
            src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
        src_file = os.path.join(src_dir, data_file)
    with open(src_file) as f:
        if format == 'json':
            data = json.load(f)
        elif format == 'yaml':
            data = yaml.load(f)
        elif format not in ['json', 'yaml'] and not key_name:
            data = f.read()
        else:
            printError('Error, argument \'key_name\' may not be used with data in %s format.' % format)
            return None
    if key_name:
        data = data[key_name]
    return data


def read_ip_ranges(filename, local_file = True, ip_only = False, conditions = []):
    """
    Returns the list of IP prefixes from an ip-ranges file

    :param filename:
    :param local_file:
    :param conditions:
    :param ip_only:
    :return:
    """
    targets = []
    data = load_data(filename, local_file = local_file)
    if 'source' in data:
        # Filtered IP ranges
        conditions = data['conditions']
        local_file = data['local_file'] if 'local_file' in data else False
        data = load_data(data['source'], local_file = local_file, key_name = 'prefixes')
    else:
        # Plain IP ranges
        data = data['prefixes']
    for d in data:
        condition_passed = True
        for condition in conditions:
            if type(condition) != list or len(condition) < 3:
                continue
            condition_passed = pass_condition(d[condition[0]], condition[1], condition[2])
            if not condition_passed:
                break
        if condition_passed:
            targets.append(d)
    if ip_only:
        ips = []
        for t in targets:
            ips.append(t['ip_prefix'])
        return ips
    else:
        return targets


def read_file(file_path, mode = 'rt'):
    """
    Read the contents of a file

    :param file_path:                   Path of the file to be read

    :return:                            Contents of the file
    """
    contents = ''
    with open(file_path, mode) as f:
        contents = f.read()
    return contents


def save_blob_as_json(filename, blob, force_write, debug):
    """
    Creates/Modifies file and saves python object as JSON

    :param filename:
    :param blob:
    :param force_write:
    :param debug:

    :return:
    """
    try:
        if prompt_4_overwrite(filename, force_write):
            with open(filename, 'wt') as f:
                print('%s' % json.dumps(blob, indent=4 if debug else None, separators=(',', ': '), sort_keys=True, cls=CustomJSONEncoder), file=f)
    except Exception as e:
        printException(e)
        pass


def save_ip_ranges(profile_name, prefixes, force_write, debug, output_format = 'json'):
    """
    Creates/Modifies an ip-range-XXX.json file

    :param profile_name:
    :param prefixes:
    :param force_write:
    :param debug:

    :return:
    """
    filename = 'ip-ranges-%s.json' % profile_name
    ip_ranges = {}
    ip_ranges['createDate'] = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # Unique prefixes
    unique_prefixes = {}
    for prefix in prefixes:
        if type(prefix) == dict:
            unique_prefixes[prefix['ip_prefix']] = prefix
        else:
            unique_prefixes[prefix] = {'ip_prefix': prefix}
    unique_prefixes = list(unique_prefixes.values())
    ip_ranges['prefixes'] = unique_prefixes
    if output_format == 'json':
        save_blob_as_json(filename, ip_ranges, force_write, debug)
    else:
        # Write as CSV
        output = 'account_id, region, ip, instance_id, instance_name\n'
        for prefix in unique_prefixes:
            output += '%s, %s, %s, %s, %s\n' % (prefix['account_id'], prefix['region'], prefix['ip_prefix'], prefix['instance_id'], prefix['name'])
        with open('ip-ranges-%s.csv' % profile_name, 'wt') as f:
            f.write(output)
