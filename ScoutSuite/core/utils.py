"""
Single-service rule processing functions
"""

import copy

from ScoutSuite.core.console import print_exception
from ScoutSuite.core.conditions import pass_conditions, fix_path_string


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
            # id_suffix
            if add_suffix and hasattr(config, 'id_suffix'):
                suffix = fix_path_string(all_info, current_path, config.id_suffix)
                current_path.append(suffix)
            # class_suffix
            if add_suffix and hasattr(config, 'class_suffix'):
                suffix = fix_path_string(all_info, current_path, config.class_suffix)
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
    elif isinstance(current_info, str):
        split_current_path = copy.deepcopy(current_path)
        results = results + recurse(all_info, current_info, [], split_current_path,
                                    config, add_suffix)
    else:
        print_exception('Unable to recursively test condition for path {}: '
                        'unhandled case for \"{}\" type'.format(current_path,
                                                                type(current_info)),
                        additional_details={'current_path': current_path,
                                            'current_info': current_info,
                                            'dbg_target_path': dbg_target_path})
    return results
