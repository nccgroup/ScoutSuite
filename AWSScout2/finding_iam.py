#!/usr/bin/env python2

from AWSScout2.finding import *

import datetime
import dateutil.parser

class IamFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level):
        self.keyword_prefix = 'iam'
        Finding.__init__(self, description, entity, callback, callback_args, level)

    def checkAccessKeys(self, key, obj):
        for access_key in obj['access_keys']:
            status = self.callback_args[0]
            self.isOlderThan90Days(key, access_key, status)

    def isOlderThan(self, key, obj, max_age, status):
        today = datetime.datetime.today()
        key_creation_date = dateutil.parser.parse(obj['create_date']).replace(tzinfo=None)
        key_age = (today - key_creation_date).days
        key_status = obj['status']
        if (key_age > max_age) and key_status == status:
            self.addItem(obj['access_key_id'], obj['user_name'])
            return True
        else:
            return False

    def isOlderThan90Days(self, key, obj, status):
        return self.isOlderThan(key, obj, 90, status)

    def lacksMFA(self, key, obj):
        if len(obj['mfa_devices']) == 0 and 'logins' in obj:
            self.addItem(obj['user_name'], obj['user_name'])
            return True
        else:
            return False

    def passwordAndKeyEnabled(self, key, obj):
        if len(obj['access_keys']) > 0 and 'logins' in obj:
            self.addItem(obj['user_name'], obj['user_name'])
            return True
        else:
            return False

    def hasUserPolicy(self, key, obj):
        if len(obj['policies']) > 0:
            self.addItem(obj['user_name'], obj['user_name'])
