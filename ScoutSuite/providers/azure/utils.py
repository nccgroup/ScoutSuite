import re


def get_resource_group_name(id):
    return re.findall("/resourceGroups/(.*?)/", id)[0]
