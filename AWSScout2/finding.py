#!/usr/bin/env python

import datetime
import dateutil.parser

class Finding():

    def __init__(self, description, entity, callback, callback_args, idprefix, level):
        self.description = description
        self.level = level
        self.entity = entity
        self.callback = callback
        self.callback_args = callback_args,
        self.idprefix = idprefix
        self.level = level
        self.items = []

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
        # FIXME: changed for dev purposes
        return self.isOlderThan(obj, 45)

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

    def checkInternetAccessiblePort(self, obj):
       return True
