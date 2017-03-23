#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import json
import os
import shutil
import sys
import zipfile

from opinel.utils import printError, printException, printInfo


########################################
# Globals
########################################

DEFAULT_REPORT_DIR = 'scout2-report'
AWSCONFIG_FILE = 'inc-awsconfig/aws_config.js'
AWSRULESET_FILE = 'inc-awsconfig/aws_ruleset.js'
EXCEPTIONS_FILE = 'inc-awsconfig/exceptions.js'
REPORT_FILE = 'report.html'



########################################
# Classes
########################################

class Scout2Encoder(json.JSONEncoder):
    """
    JSON encoder class
    """
    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return vars(o)



########################################
# Functions
########################################

def get_filename(environment_name, file_type):
    """

    :param environment_name:
    :param type:
    :return:
    """
    if file_type == 'config':
        filename = AWSCONFIG_FILE
        first_line = 'aws_info ='
    elif file_type == 'exceptions':
        filename = EXCEPTIONS_FILE
        first_line = 'exceptions ='
    elif file_type == 'report':
        filename = REPORT_FILE
        first_line = None
    elif file_type == 'ruleset':
        filename = AWSRULESET_FILE
        first_line = 'aws_info ='
    if environment_name != 'default':
        name, extention = filename.split('.')
        filename = '%s-%s.%s' % (name, environment_name, extention)
    return (filename, first_line)


def open_file(config_filename, force_write, quiet = False):
    """

    :param config_filename:
    :param force_write:
    :param quiet:
    :return:
    """
    if not quiet:
        printInfo('Saving config...')
    if prompt_4_overwrite(config_filename, force_write):
       try:
           config_dirname = os.path.dirname(config_filename)
           if not os.path.isdir(config_dirname):
               os.makedirs(config_dirname)
           return open(config_filename, 'wt')
       except Exception as e:
           printException(e)
    else:
        return None

def prepare_html_output_dir(output_dir):
        # Get path to static files
        scout2_report_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../report/data')
        # Prepare output directories
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        aws_config_dir = os.path.join(output_dir, 'inc-awsconfig')
        if not os.path.isdir(aws_config_dir):
            os.makedirs(aws_config_dir)
        # Copy static 3rd-party files
        archive = os.path.join(scout2_report_data_path, 'includes.zip')
        zip_ref = zipfile.ZipFile(archive)
        zip_ref.extractall(output_dir)
        zip_ref.close()
        # Copy static files
        inc_scout2_dir = os.path.join(output_dir, 'inc-scout2')
        src_inc_scout2_dir = os.path.join(scout2_report_data_path, 'inc-scout2')
        if os.path.isdir(inc_scout2_dir):
            shutil.rmtree(inc_scout2_dir)
        shutil.copytree(src_inc_scout2_dir, inc_scout2_dir)


def prompt_4_yes_no(question):
    """
    Ask a question and prompt for yes or no

    :param question:                    Question to ask; answer is yes/no
    :return:                            :boolean
    """
    while True:
        sys.stdout.write(question + ' (y/n)? ')
        try:
            choice = raw_input().lower()
        except:
            choice = input().lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            printError('\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice)


def prompt_4_overwrite(filename, force_write):
    """
    Confirm before overwriting existing files. Do not prompt if the file does not exist or force_write is set

    :param filename:                    Name of the file to be overwritten
    :param force_write:                 Do not ask for confirmation and automatically return True if set
    :return:                            :boolean
    """
    #
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_4_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename))


def save_config_to_file(environment_name, aws_config, config_type, output_dir, force_write, debug):
    """

    :param aws_config:
    :param config_type:
    :param output_dir:
    :param force_write:
    :param debug:
    :return:
    """
    config_file, first_line = get_filename(environment_name, config_type)
    config_path = os.path.join(output_dir, config_file)
    #try:
    with open_file(config_path, force_write, False) as f:
        if first_line:
            print('%s' % first_line, file=f)
        print('%s' % json.dumps(aws_config, indent=4 if debug else None, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder), file=f)
