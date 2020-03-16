from __future__ import print_function

import datetime
import json
import os

from ScoutSuite.core.console import print_exception, prompt_overwrite, print_info
from ScoutSuite.core.conditions import pass_condition


class CustomJSONEncoder(json.JSONEncoder):
    """
    JSON encoder class
    """

    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return o.__dict__


def load_data(data_file, key_name=None, local_file=False):
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
        src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
        src_file = os.path.join(src_dir, data_file)
    with open(src_file) as f:
        data = json.load(f)
    if key_name:
        data = data[key_name]
    return data


def read_ip_ranges(filename, local_file=True, ip_only=False, conditions=None):
    """
    Returns the list of IP prefixes from an ip-ranges file

    :param filename:
    :param local_file:
    :param conditions:
    :param ip_only:
    :return:
    """
    if not conditions:
        conditions = []

    targets = []
    data = load_data(filename, local_file=local_file)
    if 'source' in data:
        # Filtered IP ranges
        conditions = data['conditions']
        local_file = data['local_file'] if 'local_file' in data else False
        data = load_data(data['source'], local_file=local_file, key_name='prefixes')
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


def save_blob_as_json(filename, blob, force_write):
    """
    Creates/Modifies file and saves python object as JSON

    :param filename:
    :param blob:
    :param force_write:

    :return:
    """
    try:
        if prompt_overwrite(filename, force_write):
            with open(filename, 'wt') as f:
                print_info('%s' % json.dumps(blob, indent=4, separators=(',', ': '), sort_keys=True,
                                             cls=CustomJSONEncoder))
    except Exception as e:
        print_exception(e)
