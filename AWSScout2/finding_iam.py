#!/usr/bin/env python

from AWSScout2.finding import *

import datetime
import dateutil.parser

class IamFinding(Finding):

    def __init__(self, description, name, entity, callback, callback_args, idprefix, level):
        self.keyword_prefix = 'iam'
        Finding.__init__(self, description, name, entity, callback, callback_args, idprefix, level)

    def checkAccessKeys(self, obj):
        for access_key in obj['access_keys']:
            self.isOlderThan90Days(access_key)

    def isOlderThan(self, obj, max_age):
        today = datetime.datetime.today()
        key_creation_date = dateutil.parser.parse(obj['create_date']).replace(tzinfo=None)
        key_age = (today - key_creation_date).days
        if (key_age > max_age):
            self.items.append(obj['access_key_id'])
            return True
        else:
            return False

    def isOlderThan90Days(self, obj):
        return self.isOlderThan(obj, 90)

    def lacksMFA(self, obj):
        if len(obj['mfa_devices']) == 0 and 'logins' in obj:
            self.items.append(obj['user_name'])
            return True
        else:
            return False

    def passwordAndKeyEnabled(self, obj):
        if len(obj['access_keys']) > 0 and 'logins' in obj:
            self.items.append(obj['user_name'])
            return True
        else:
            return False
