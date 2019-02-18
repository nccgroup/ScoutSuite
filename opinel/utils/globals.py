#                            -*- coding: utf-8 -*-
                            
import boto3
from distutils.version import StrictVersion
import os
import re

from opinel import __version__ as OPINEL_VERSION
from opinel.utils.console import printError


########################################
# Regex
########################################

re_opinel = re.compile(r'^opinel>=([0-9.]+),<([0-9.]+).*')
re_boto3 = re.compile(r'^boto3>=([0-9.]+)(,<([0-9.]+).*)?')


########################################
# Functions
########################################

def check_requirements(script_path, requirements_file = None):
    """
    Check versions of opinel and boto3
    :param script_path:
    :return:
    """
    script_dir = os.path.dirname(script_path)
    opinel_min_version = opinel_max_version = boto3_min_version = boto3_max_version = None
    # Requirements file is either next to the script or in data/requirements
    if not requirements_file:
        requirements_file = os.path.join(script_dir, 'data/requirements.txt')
        if not os.path.isfile(requirements_file):
            requirements_file = os.path.join(script_dir, 'requirements.txt')
    with open(requirements_file, 'rt') as f:
        for requirement in f.readlines():
            opinel_requirements = re_opinel.match(requirement)
            if opinel_requirements:
                opinel_requirements = opinel_requirements.groups()
                opinel_min_version = opinel_requirements[0]
                opinel_max_version = opinel_requirements[1]
            boto3_requirements = re_boto3.match(requirement)
            if boto3_requirements:
                boto3_requirements = boto3_requirements.groups()
                boto3_min_version = boto3_requirements[0]
                boto3_max_version = boto3_requirements[1]
    if not check_versions(opinel_min_version, OPINEL_VERSION, opinel_max_version, 'opinel'):
        return False
    if not check_versions(boto3_min_version, boto3.__version__, boto3_max_version, 'boto3'):
        return False
    return True


def check_versions(min_version, installed_version, max_version, package_name, strict = False):
    """

    :param min_version:
    :param installed_version:
    :param max_version:
    :param package_name:

    :return:
    """
    if not min_version:
        # If no minimum version was specified, pass
        return True
    if StrictVersion(installed_version) < StrictVersion(min_version):
        printError('Error: the version of %s installed on this system (%s) is too old. '
                   'You need at least version %s to run this tool.' % (package_name, OPINEL_VERSION, min_version))
        return False
    if max_version and StrictVersion(installed_version) >= StrictVersion(max_version):
        printError('Warning: ther version of %s installed on this system (%s) is too recent; '
                   'you may experience unexpected runtime errors as versions above %s have not been tested.' %
                   (package_name, installed_version, max_version))
        if strict:
            printError('Warning treated as error.')
            return False
    return True


def manage_dictionary(dictionary, key, init, callback = None):
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


def snake_to_camel(snake):
    return "".join(val.title() for val in snake.split('_'))

def snake_to_words(snake, capitalize = False):
    return " ".join(val.title() if capitalize else val for val in snake.split('_'))
