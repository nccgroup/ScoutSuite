# -*- coding: utf-8 -*-
from __future__ import print_function

from ScoutSuite.providers.aws.utils import formatted_service_name


def manage_dictionary(dictionary, key, init, callback=None):
    """

    :param dictionary:
    :param key:
    :param init:
    :param callback:

    :return:
    """
    if not str(key) in dictionary:
        dictionary[str(key)] = init
        manage_dictionary(dictionary, key, init)
        if callback:
            callback(dictionary[key])
    return dictionary


def format_service_name(service):
    """

    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()
