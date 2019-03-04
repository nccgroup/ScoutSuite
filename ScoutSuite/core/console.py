# -*- coding: utf-8 -*-

import os
import re
import sys
import traceback

from six.moves import input

########################################
# Globals
########################################

mfa_serial_format = r'^arn:aws:iam::\d+:mfa/[a-zA-Z0-9\+=,.@_-]+$'
re_mfa_serial_format = re.compile(mfa_serial_format)
re_mfa_code = r'^\d{6}\d*$'


########################################
# Print configuration functions
########################################

def config_debug_level(enable):
    """
    Configure whether full stacktraces should be dumped in the console output

    :param enable:

    :return:
    """
    global verbose_exceptions
    verbose_exceptions = enable


########################################
# Print functions
########################################

def print_debug(msg):
    if verbose_exceptions:
        print_generic(sys.stderr, msg)


def print_error(msg, new_line=True):
    print_generic(sys.stderr, msg, new_line)


def print_exception(e, debug_only=False):
    global verbose_exceptions
    if verbose_exceptions:
        print_error(str(traceback.format_exc()))
    elif not debug_only:
        print_error(str(e))


def print_generic(out, msg, new_line=True):
    out.write(msg)
    out.flush()
    if new_line:
        out.write('\n')


def print_info(msg, new_line=True):
    print_generic(sys.stdout, msg, new_line)


########################################
# Prompt functions
########################################

def prompt(test_input=None):
    """
    Prompt function that works for Python2 and Python3

    :param test_input:                  Value to be returned when testing

    :return:                            Value typed by user (or passed in argument when testing)
    """
    if test_input is not None:
        if type(test_input) == list and len(test_input):
            choice = test_input.pop(0)
        elif type(test_input) == list:
            choice = ''
        else:
            choice = test_input
    else:
        choice = input()
    return choice


def prompt_mfa_code(activate=False, test_input=None):
    """
    Prompt for an MFA code

    :param activate:                    Set to true when prompting for the 2nd code when activating a new MFA device
    :param test_input:                       Used for unit testing

    :return:                            The MFA code
    """
    while True:
        if activate:
            prompt_string = 'Enter the next value: '
        else:
            prompt_string = 'Enter your MFA code (or \'q\' to abort): '
        mfa_code = prompt_value(prompt_string, no_confirm=True, test_input=test_input)
        if mfa_code == 'q':
            return mfa_code
        if not re.match(re_mfa_code, mfa_code):
            print_error('Error: your MFA code must only consist of digits and be at least 6 characters long.')
        break
    return mfa_code


def prompt_overwrite(filename, force_write, test_input=None):
    """
    Prompt whether the file should be overwritten

    :param filename:                    Name of the file about to be written
    :param force_write:                 Skip confirmation prompt if this flag is set
    :param test_input:                       Used for unit testing

    :return:                            Boolean whether file write operation is allowed
    """
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename),
                         test_input=test_input)


def prompt_value(question, choices=None, default=None, display_choices=True, display_indices=False,
                 authorize_list=False, is_question=False, no_confirm=False, required=True, regex=None,
                 regex_format='', max_laps=5, test_input=None, return_index=False):
    """
    Prompt for a value
                                        .                    .
    :param return_index:
    :param question:                    Question to be asked
    :param choices:                     List of authorized answers
    :param default:                     Value suggested by default
    :param display_choices:             Display accepted choices
    :param display_indices:             Display the indice in the list next to the choice
    :param authorize_list:              Set to true if a list of answers may be accepted
    :param is_question:                 Set to true to append a question mark
    :param no_confirm:                  Set to true to not prompt for a confirmation of the value
    :param required:                    Set to false if an empty answer is authorized
    :param regex:                       TODO
    :param regex_format                 TODO
    :param max_laps:                    Exit after N laps
    :param test_input:                  Used for unit testing
    :param return_index                 TODO

    :return:
    """
    int_choice = 0

    if choices and display_choices and not display_indices:
        question = question + ' (' + '/'.join(choices) + ')'
    lap_n = 0
    while True:
        if lap_n >= max_laps:
            print_error('Automatically aborting prompt loop after 5 failures')
            return None
        lap_n += 1
        can_return = False
        # Display the question, choices, and prompt for the answer
        if is_question:
            question = question + '? '
        print_error(question)
        if choices and display_indices:
            for c in choices:
                print_error('%3d. %s' % (choices.index(c), c))
            print_error('Enter the number corresponding to your choice: ', False)
        choice = prompt(test_input)
        # Set the default value if empty choice
        if not choice or choice == '':
            if default:
                if no_confirm or prompt_yes_no('Use the default value (' + default + ')'):
                    # return default
                    choice = default
                    can_return = True
            elif not required:
                can_return = True
            else:
                print_error('Error: you cannot leave this parameter empty.')
        # Validate the value against a whitelist of choices
        elif choices:
            user_choices = [item.strip() for item in choice.split(',')]
            if not authorize_list and len(user_choices) > 1:
                print_error('Error: multiple values are not supported; please enter a single value.')
            else:
                choice_valid = True
                if display_indices and int(choice) < len(choices):
                    int_choice = choice
                    choice = choices[int(choice)]
                else:
                    for c in user_choices:
                        if c not in choices:
                            print_error('Invalid value (%s).' % c)
                            choice_valid = False
                            break
                if choice_valid:
                    can_return = True
        # Validate against a regex
        elif regex:
            if regex.match(choice):
                # return choice
                can_return = True
            else:
                print_error('Error: expected format is: %s' % regex_format)
        else:
            # No automated validation, can attempt to return
            can_return = True
        if can_return:
            # Manually confirm that the entered value is correct if needed
            if no_confirm or prompt_yes_no('You entered "' + choice + '". Is that correct', test_input=test_input):
                return int(int_choice) if return_index else choice


def prompt_yes_no(question, test_input=None):
    """
    Prompt for a yes/no or y/n answer
                                        .
    :param question:                    Question to be asked
    :param test_input:                  Used for unit testing

    :return:                            True for yes/y, False for no/n
    """
    count = 0
    while True:
        print_error(question + ' (y/n)? ')
        choice = prompt(test_input).lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            count += 1
            print_error('\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice)
            if count > 3:
                return None
