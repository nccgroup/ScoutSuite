# -*- coding: utf-8 -*-

import os
import re
import sys
import traceback

try:
    input = raw_input
except NameError: pass


########################################
# Globals
########################################

mfa_serial_format = r'^arn:aws:iam::\d+:mfa/[a-zA-Z0-9\+=,.@_-]+$'
re_mfa_serial_format = re.compile(mfa_serial_format)



########################################
# Print configuration functions
########################################

def configPrintException(enable):
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

def printDebug(msg):
    if verbose_exceptions:
        printGeneric(sys.stderr, msg)


def printError(msg, newLine = True):
    printGeneric(sys.stderr, msg, newLine)


def printException(e, debug_only = False):
    global verbose_exceptions
    if verbose_exceptions:
        printError(str(traceback.format_exc()))
    elif not debug_only:
        printError(str(e))


def printGeneric(out, msg, newLine = True):
    out.write(msg)
    out.flush()
    if newLine == True:
        out.write('\n')


def printInfo(msg, newLine = True ):
    printGeneric(sys.stdout, msg, newLine)



########################################
# Prompt functions
########################################

def prompt(test_input = None):
    """
    Prompt function that works for Python2 and Python3

    :param test_input:                  Value to be returned when testing

    :return:                            Value typed by user (or passed in argument when testing)
    """
    if test_input != None:
        if type(test_input) == list and len(test_input):
            choice = test_input.pop(0)
        elif type(test_input) == list:
            choice = ''
        else:
            choice = test_input
    else:
        # Coverage: 4 missed statements
        try:
            choice = input()
        except:
            choice = input()
    return choice


def prompt_4_mfa_code(activate = False, input = None):
    """
    Prompt for an MFA code

    :param activate:                    Set to true when prompting for the 2nd code when activating a new MFA device
    :param input:                       Used for unit testing

    :return:                            The MFA code
    """
    while True:
        if activate:
            prompt_string = 'Enter the next value: '
        else:
            prompt_string = 'Enter your MFA code (or \'q\' to abort): '
        mfa_code = prompt_4_value(prompt_string, no_confirm = True, input = input)
        try:
            if mfa_code == 'q':
                return mfa_code
            int(mfa_code)
            mfa_code[5]
            break
        except:
            printError('Error: your MFA code must only consist of digits and be at least 6 characters long.')
    return mfa_code


def prompt_4_mfa_serial(input = None):
    """
    Prompt for an MFA serial number

    :param input:                       Used for unit testing

    :return:                            The MFA serial number
    """
    return prompt_4_value('Enter your MFA serial:', required = False, regex = re_mfa_serial_format, regex_format = mfa_serial_format, input = input)


def prompt_4_overwrite(filename, force_write, input = None):
    """
    Prompt whether the file should be overwritten

    :param filename:                    Name of the file about to be written
    :param force_write:                 Skip confirmation prompt if this flag is set
    :param input:                       Used for unit testing

    :return:                            Boolean whether file write operation is allowed
    """
    if not os.path.exists(filename) or force_write:
        return True
    return prompt_4_yes_no('File \'{}\' already exists. Do you want to overwrite it'.format(filename), input = input)


def prompt_4_value(question, choices = None, default = None, display_choices = True, display_indices = False, authorize_list = False, is_question = False, no_confirm = False, required = True, regex = None, regex_format = '', max_laps = 5, input = None, return_index = False):
    """
    Prompt for a value
                                        .                    .
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
    :param input:                       Used for unit testing

    :return:
    """
    if choices and display_choices and not display_indices:
        question = question + ' (' + '/'.join(choices) + ')'
    lap_n = 0
    while True:
        if lap_n >= max_laps:
            printError('Automatically abording prompt loop after 5 failures')
            return None
        lap_n += 1
        can_return = False
        # Display the question, choices, and prompt for the answer
        if is_question:
            question = question + '? '
        printError(question)
        if choices and display_indices:
            for c in choices:
                printError('%3d. %s' % (choices.index(c), c))
            printError('Enter the number corresponding to your choice: ', False)
        choice = prompt(input)
        # Set the default value if empty choice
        if not choice or choice == '':
            if default:
                if no_confirm or prompt_4_yes_no('Use the default value (' + default + ')'):
                    #return default
                    choice = default
                    can_return = True
            elif not required:
                can_return = True
            else:
                printError('Error: you cannot leave this parameter empty.')
        # Validate the value against a whitelist of choices
        elif choices:
            user_choices = [item.strip() for item in choice.split(',')]
            if not authorize_list and len(user_choices) > 1:
                printError('Error: multiple values are not supported; please enter a single value.')
            else:
                choice_valid = True
                if display_indices and int(choice) < len(choices):
                    int_choice = choice
                    choice = choices[int(choice)]
                else:
                    for c in user_choices:
                        if not c in choices:
                            printError('Invalid value (%s).' % c)
                            choice_valid = False
                            break
                if choice_valid:
                    can_return = True
        # Validate against a regex
        elif regex:
            if regex.match(choice):
                #return choice
                can_return = True
            else:
                printError('Error: expected format is: %s' % regex_format)
        else:
            # No automated validation, can attempt to return
            can_return = True
        if can_return:
            # Manually onfirm that the entered value is correct if needed
            if no_confirm or prompt_4_yes_no('You entered "' + choice + '". Is that correct', input=input):
                return int(int_choice) if return_index else choice


def prompt_4_yes_no(question, input = None):
    """
    Prompt for a yes/no or y/n answer
                                        .
    :param question:                    Question to be asked
    :param input:                       Used for unit testing

    :return:                            True for yes/y, False for no/n
    """
    count = 0
    while True:
        printError(question + ' (y/n)? ')
        choice = prompt(input).lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            count += 1
            printError('\'%s\' is not a valid answer. Enter \'yes\'(y) or \'no\'(n).' % choice)
            if count > 3:
                return None
