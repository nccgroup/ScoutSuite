# -*- coding: utf-8 -*-
"""
Single-service rule processing functions
"""

from six import string_types
import copy
import re

from opinel.utils.conditions import pass_condition
from opinel.utils.console import printError, printException

from ScoutSuite.core import condition_operators
from ScoutSuite.providers.base.configs.browser import get_value_at

re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')
re_nested_get_value_at = re.compile(r'_GET_VALUE_AT_\(.*')


def fix_path_string(all_info, current_path, path_to_value):
    # handle nested _GET_VALUE_AT_...
    while True:
        dynamic_path = re_get_value_at.findall(path_to_value)
        if len(dynamic_path) == 0:
            break
        for dp in dynamic_path:
            tmp = dp
            while True:
                nested = re_nested_get_value_at.findall(tmp)
                if len(nested) == 0:
                    break
                tmp = nested[0].replace('_GET_VALUE_AT_(', '', 1)
            dv = get_value_at(all_info, current_path, tmp)
            path_to_value = path_to_value.replace('_GET_VALUE_AT_(%s)' % tmp, dv)
    return path_to_value


def recurse(all_info, current_info, target_path, current_path, config, add_suffix=False):
    """
    Recursively test conditions for a path.
    In order to do this, needs to evaluate all the `id` possibilities.

    When the value in the path is `id`, this represents either a key for a dict or an index for a list.

    When the is `id`:
    - For a dict return value at key
    - For a list, return the list
    When the value ends in `id.`:
    - For a dict, return a list of keys
    - For a list, return value at the index indicated by id
    `
    :param all_info:        All of the services' data
    :param current_info:    ?
    :param target_path:     The path that is being tested
    :param current_path:
    :param config:          The Rule object that is being tested
    :param add_suffix:      ?
    :return:
    """
    results = []
    if len(target_path) == 0:
        # Dashboard: count the number of processed resources here
        setattr(config, 'checked_items', getattr(config, 'checked_items') + 1)
        # Test for conditions...
        if pass_conditions(all_info, current_path, copy.deepcopy(config.conditions)):
            if add_suffix and hasattr(config, 'id_suffix'):
                suffix = fix_path_string(all_info, current_path, config.id_suffix)
                current_path.append(suffix)
            results.append('.'.join(current_path))
        # Return the flagged items...
        return results
    target_path = copy.deepcopy(target_path)
    dbg_target_path = copy.deepcopy(target_path)
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
                results = results + recurse(all_info, split_current_info, split_target_path, split_current_path,
                                            config, add_suffix)
    # To handle lists properly, I would have to make sure the list is properly ordered and I can use the index to
    # consistently access an object... Investigate (or do not use lists)
    elif type(current_info) == list:
        for index, split_current_info in enumerate(current_info):
            split_current_path = copy.deepcopy(current_path)
            split_current_path.append(str(index))
            results = results + recurse(all_info, split_current_info, copy.deepcopy(target_path), split_current_path,
                                        config, add_suffix)
    # Python 2-3 compatible way to check for string type
    elif isinstance(current_info, string_types):
        split_current_path = copy.deepcopy(current_path)
        results = results + recurse(all_info, current_info, [], split_current_path,
                                    config, add_suffix)
    else:
        printError('Error: unhandled case, typeof(current_info) = %s' % type(current_info))
        printError('Path: %s' % current_path)
        printError('Object: %s' % str(current_info))
        printError('Entry target path: %s' % str(dbg_target_path))
        raise Exception
    return results


def pass_conditions(all_info, current_path, conditions, unknown_as_pass_condition=False):
    """
    Check that all conditions are passed for the current path.

    :param all_info:        All of the services' data
    :param current_path:    The value of the `path` variable defined in the finding file
    :param conditions:      The conditions to check as defined in the finding file
    :param unknown_as_pass_condition:   Consider an undetermined condition as passed
    :return:
    """
    result = False
    if len(conditions) == 0:
        return True
    condition_operator = conditions.pop(0)
    for condition in conditions:
        if condition[0] in condition_operators:
            res = pass_conditions(all_info, current_path, condition, unknown_as_pass_condition)
        else:
            # Conditions are formed as "path to value", "type of test", "value(s) for test"
            path_to_value, test_name, test_values = condition
            path_to_value = fix_path_string(all_info, current_path, path_to_value)
            target_obj = get_value_at(all_info, current_path, path_to_value)
            if type(test_values) != list:
                dynamic_value = re_get_value_at.match(test_values)
                if dynamic_value:
                    test_values = get_value_at(all_info, current_path, dynamic_value.groups()[0], True)
            try:
                res = pass_condition(target_obj, test_name, test_values)
            except Exception as e:
                res = True if unknown_as_pass_condition else False
                printError('Unable to process testcase \'%s\' on value \'%s\', interpreted as %s.' % (
                    test_name, str(target_obj), res))
                printException(e, True)
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
