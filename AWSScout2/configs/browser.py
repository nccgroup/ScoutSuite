# -*- coding: utf-8 -*-

import copy

from opinel.utils.console import printError, printException

########################################
# Functions
########################################

def combine_paths(path1, path2):
    path = path1
    for p in path2:
        if p == '..':
            del(path[-1])
        else:
            path.append(p)
    return path

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
