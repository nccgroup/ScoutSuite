# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys

from ScoutSuite.core.console import print_error

from six.moves import input

from ScoutSuite.output.report_file import ReportFile


def prompt_for_yes_no(question):
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
            print_error('\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice)


def prompt_for_overwrite(filename, force_write):
    """
    Confirm before overwriting existing files. Do not prompt if the file does not exist or force_write is set

    :param filename:                    Name of the file to be overwritten
    :param force_write:                 Do not ask for confirmation and automatically return True if set
    :return:                            :boolean
    """
    #
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_for_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename))


def get_filename(config_type, profile, report_dir, extension=None):
        if config_type == ReportFile.AWSCONFIG:
            filename = ReportFile.AWSCONFIG.value
            first_line = 'scoutsuite_results ='
        elif config_type == ReportFile.EXCEPTIONS:
            filename = ReportFile.EXCEPTIONS.value
            first_line = 'exceptions ='
        elif config_type == ReportFile.HTMLREPORT:
            filename = ReportFile.HTMLREPORT.value
            first_line = None
        elif config_type == ReportFile.AWSRULESET:
            filename = ReportFile.AWSRULESET.value
            first_line = 'scoutsuite_results ='
        else:
            print_error('invalid config type provided (%s)' % config_type)
            raise Exception
        # Append profile name if necessary
        if profile != 'default' and config_type != ReportFile.AWSRULESET:
            name, original_extension = filename.split('.')
            extension = extension if extension else original_extension
            filename = '%s-%s.%s' % (name, profile, extension)
        return os.path.join(report_dir, filename), first_line
