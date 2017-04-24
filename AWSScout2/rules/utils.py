# -*- coding: utf-8 -*-
"""
Single-service rule processing functions
"""

import copy
import re

from opinel.utils.conditions import pass_condition
from opinel.utils.console import printError
from opinel.utils.globals import manage_dictionary

from AWSScout2.rules import condition_operators
from AWSScout2.configs.browser import get_value_at



re_get_value_at = re.compile(r'_GET_VALUE_AT_\((.*?)\)')


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
