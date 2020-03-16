import copy

from ScoutSuite.core.console import print_exception


########################################
# Functions
########################################

def combine_paths(path1, path2):
    path = path1
    for p in path2:
        if p == '..':
            del (path[-1])
        else:
            path.append(p)
    return path


def get_object_at(object, path, attribute_name=None):
    """
    Get arbitrary object given a dictionary and path (list of keys).

    :param object:
    :param path:
    :param attribute_name:
    :return:
    """
    o = object
    try:
        for p in path:
            if type(o) is dict:
                o = o[p]
            else:
                o = getattr(o, p)

        if attribute_name:
            if type(o) is dict:
                return o[attribute_name]
            else:
                return getattr(o, attribute_name)
        else:
            return o
    except Exception as e:
        raise Exception


def get_value_at(all_info, current_path, key, to_string=False):
    """
    Get value located at a given path.

    :param all_info:        All of the services' data
    :param current_path:    The value of the `path` variable defined in the finding file
    :param key:             The key that is being requested
    :param to_string:       Whether or not the returned value should be casted as a string
    :return:                The value in `all_info` indicated by the `key` in `current_path`
    """
    keys = key.split('.')
    if keys[-1] == 'id':
        target_obj = current_path[len(keys) - 1]
    else:
        if key == 'this':
            target_path = current_path
        elif '.' in key:
            target_path = []
            for i, key in enumerate(keys):
                # If 'id', replace by value
                if key == 'id':
                    target_path.append(current_path[i])
                # If empty key and value is an index, keep the index
                elif key == '' and i < len(current_path) and current_path[i].isdigit():
                    target_path.append(int(current_path[i]))
                # Otherwise, use key
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
                # TODO ensure this additional condition didn't break anything
                elif type(target_obj) == list and type(p) == int:
                    target_obj = target_obj[p]
                elif type(target_obj) == list and p.isdigit():
                    target_obj = target_obj[int(p)]
                elif type(target_obj) == list:
                    target_obj = p
                elif p == '':
                    pass
                else:
                    target_obj = target_obj[p]
            except Exception as e:
                print_exception(e, additional_details={'current_path': current_path})
                # raise Exception
    if to_string:
        return str(target_obj)
    else:
        return target_obj
