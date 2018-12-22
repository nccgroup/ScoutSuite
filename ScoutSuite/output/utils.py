# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys

from opinel.utils.console import printError

from six.moves import input

from ScoutSuite import AWSCONFIG, EXCEPTIONS, HTMLREPORT, AWSRULESET, AWSCONFIG_FILE, EXCEPTIONS_FILE, HTMLREPORT_FILE, AWSRULESET_FILE


def prompt_4_yes_no(question):
    """
    Ask a question and prompt for yes or no

    :param question:                    Question to ask; answer is yes/no
    :return:                            :boolean
    """

    while True:
        sys.stdout.write(question + ' (y/n)? ')
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


def get_filename(config_type, profile, report_dir):
        if config_type == AWSCONFIG:
            filename = AWSCONFIG_FILE
            first_line = 'scoutsuite_results ='
        elif config_type == EXCEPTIONS:
            filename = EXCEPTIONS_FILE
            first_line = 'exceptions ='
        elif config_type == HTMLREPORT:
            filename = HTMLREPORT_FILE
            first_line = None
        elif config_type == AWSRULESET:
            filename = AWSRULESET_FILE
            first_line = 'scoutsuite_results ='
        else:
            printError('invalid config type provided (%s)' % config_type)
            raise Exception
        # Append profile name if necessary
        if profile != 'default' and config_type != AWSRULESET:
            name, extention = filename.split('.')
            filename = '%s-%s.%s' % (name, profile, extention)
        return (os.path.join(report_dir, filename), first_line)
