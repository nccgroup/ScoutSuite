# -*- coding: utf-8 -*-

import datetime
import dateutil.parser
import json
import netaddr
import re

from opinel.utils.console import printError

from iampoliciesgonewild import get_actions_from_statement, _expand_wildcard_action



def __prepare_age_test(a, b):
    if type(a) != list:
        printError('Error: olderThan requires a list such as [ N , \'days\' ] or [ M, \'hours\'].')
        raise Exception
    number = int(a[0])
    unit = a[1]
    if unit not in ['days', 'hours', 'minutes', 'seconds']:
        printError('Error: only days, hours, minutes, and seconds are supported.')
        raise Exception
    if unit == 'hours':
        number *= 3600
        unit = 'seconds'
    elif unit == 'minutes':
        number *= 60
        unit = 'seconds'
    age = getattr((datetime.datetime.today() - dateutil.parser.parse(str(b)).replace(tzinfo=None)), unit)
    return age, number


def pass_condition(b, test, a):
    """
    Generic test function used by Scout2 / AWS recipes
                                        .
    :param b:                           Value to be tested against
    :param test:                        Name of the test case to run
    :param a:                           Value to be tested

    :return:                            True of condition is met, False otherwise
    """

    # Return false by default
    result = False

    # Equality tests
    if test == 'equal':
        a = str(a)
        b = str(b)
        result = (a == b)
    elif test == 'notEqual':
        result = (not pass_condition(b, 'equal', a))

    # More/Less tests
    elif test == 'lessThan':
        result = (int(b) < int(a))
    elif test == 'lessOrEqual':
        result = (int(b) <= int(a))
    elif test == 'moreThan':
        result = (int(b) > int(a))
    elif test == 'moreOrEqual':
        result = (int(b) >= int(a))

    # Empty tests
    elif test == 'empty':
        result = ((type(b) == dict and b == {}) or (type(b) == list and b == []) or (type(b) == list and b == [None]))
    elif test == 'notEmpty':
        result = (not pass_condition(b, 'empty', 'a'))
    elif test == 'null':
        result = ((b == None) or (type(b) == str and b == 'None'))
    elif test == 'notNull':
        result = (not pass_condition(b, 'null', a))

    # Boolean tests
    elif test == 'true':
        result = (str(b).lower() == 'true')
    elif test == 'notTrue' or test == 'false':
        result = (str(b).lower() == 'false')

    # Object length tests
    elif test == 'lengthLessThan':
        result = (len(b) < int(a))
    elif test == 'lengthMoreThan':
        result = (len(b) > int(a))
    elif test == 'lengthEqual':
        result = (len(b) == int(a))

    # Dictionary keys tests
    elif test == 'withKey':
        result = (a in b)
    elif test == 'withoutKey':
        result = (not a in b)

    # List tests
    elif test == 'containAtLeastOneOf':
        result = False
        if not type(b) == list:
            b = [ b ]
        if not type(a) == list:
            a = [ a ]
        for c in b:
            if type(c):
                c = str(c)
            if c in a:
                result = True
                break
    elif test == 'containAtLeastOneDifferentFrom':
        result = False
        if not type(b) == list:
            b = [ b ]
        if not type(a) == list:
            a = [ a ]
        for c in b:
            if c != None and c != '' and c not in a:
                result = True
                break
    elif test == 'containNoneOf':
        result = True
        if not type(b) == list:
            b = [ b ]
        if not type(a) == list:
            a = [ a ]
        for c in b:
            if c in a:
                result = False
                break

    # Regex tests
    elif test == 'match':
        if type(a) != list:
            a = [ a ]
        b = str(b)
        for c in a:
            if re.match(c, b) != None:
                result = True
                break
    elif test == 'notMatch':
        result = (not pass_condition(b, 'match', a))

    # Date tests
    elif test == 'priorToDate':
        b = dateutil.parser.parse(str(b)).replace(tzinfo=None)
        a = dateutil.parser.parse(str(a)).replace(tzinfo=None)
        result = (b < a)
    elif test == 'olderThan':
        age, threshold = __prepare_age_test(a, b)
        result = (age > threshold)
    elif test == 'newerThan':
        age, threshold = __prepare_age_test(a, b)
        result = (age < threshold)

    # CIDR tests
    elif test == 'inSubnets':
        result = False
        grant = netaddr.IPNetwork(b)
        if type(a) != list:
            a = [ a ]
        for c in a:
            known_subnet = netaddr.IPNetwork(c)
            if grant in known_subnet:
                result = True
                break
    elif test == 'notInSubnets':
        result = (not pass_condition(b, 'inSubnets', a))

    # Policy statement tests
    elif test == 'containAction':
        result = False
        if type(b) != dict:
            b = json.loads(b)
        statement_actions = get_actions_from_statement(b)
        rule_actions = _expand_wildcard_action(a)
        for action in rule_actions:
            if action.lower() in statement_actions:
                result = True
                break
    elif test == 'notContainAction':
        result = (not pass_condition(b, 'containAction', a))
    elif test == 'containAtLeastOneAction':
        result = False
        if type(b) != dict:
            b = json.loads(b)
        if type(a) != list:
            a = [ a ]
        actions = get_actions_from_statement(b)
        for c in a:
            if c.lower() in actions:
                result = True
                break

    # Policy principal tests
    elif test == 'isCrossAccount':
        result = False
        if type(b) != list:
            b = [b]
        for c in b:
            if c != a and not re.match(r'arn:aws:iam:.*?:%s:.*' % a, c):
                result = True
                break
    elif test == 'isSameAccount':
        result = False
        if type(b) != list:
            b = [b]
        for c in b:
            if c == a or re.match(r'arn:aws:iam:.*?:%s:.*' % a, c):
                result = True
                break

    # Unknown test case
    else:
        printError('Error: unknown test case %s' % test)
        raise Exception

    return result
