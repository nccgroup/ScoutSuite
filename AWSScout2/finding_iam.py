#!/usr/bin/env python2

from AWSScout2.finding import *

import datetime
import dateutil.parser

class IamFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'iam'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)

    def checkAccessKeys(self, key, obj):
        for access_key in obj['access_keys']:
            status = self.callback_args[0]
            if len(self.callback_args) > 1:
                max_age = int(self.callback_args[1])
            else:
                max_age = 90
            self.isOlderThan(key, access_key, max_age, status)

    def belongsToGroup(self, key, obj):
        for group in obj['groups']:
            if group['group_name'] == self.callback_args[0]:
                return
        self.addItem(obj['user_name'])

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

    def lacksMFA(self, key, obj):
        if len(obj['mfa_devices']) == 0 and 'logins' in obj:
            self.addItem(obj['user_name'])
            return True
        else:
            return False

    def passwordAndKeyEnabled(self, key, obj):
        if len(obj['access_keys']) > 0 and 'logins' in obj:
            self.addItem(obj['user_name'])
            return True
        else:
            return False

    def hasUserPolicy(self, key, obj):
        if len(obj['policies']) > 0:
            self.addItem(obj['user_name'])
