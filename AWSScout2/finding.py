#!/usr/bin/env python

import datetime
import dateutil.parser
import re

class Finding():

    re_port_range = re.compile(r'(\d+)\-(\d+)')
    re_single_port = re.compile(r'(\d+)')

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
        protocol = self.callback_args[0][0].lower()
        port = self.callback_args[0][1]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if grant == '0.0.0.0/0' and self.portInRange(port, rule['ports']):
                        self.items.append(obj['id'] + '-' + protocol.upper() + '-' + port + '-' + grant)

    def checkOpenPort(self, obj):
        protocol = self.callback_args[0][0].lower()
        port = self.callback_args[0][1]
        if protocol in obj['protocols']:
            for rule in obj['protocols'][protocol]['rules']:
                for grant in rule['grants']:
                    if self.portInRange(port, rule['ports']):
                        self.items.append(obj['id'] + '-' + protocol.upper() + '-' + port)

    def portInRange(self, port, ports):
        result = self.re_port_range.match(ports)
        if result:
            p1 = int(result.group(1))
            p2 = int(result.group(2))
            if int(port) in range(int(result.group(1)), int(result.group(2))):
                return True
        else:
            result = self.re_single_port.match(ports)
            if result and port == result.group(1):
                return True
        return False

    def checkWorldWritableBucket(self, obj):
        for grant in obj['grants']:
            if 'All users' in grant:
                if obj['grants']['All users']['write']:
                    self.items.append('s3-bucket-write-' + grant + '-' + obj['name'])
                if obj['grants']['All users']['write_acp']:
                    self.items.append('s3-bucket-write_acp-' + grant + '-' + obj['name'])

    def checkWorldReadableBucket(self, obj):
        for grant in obj['grants']:
            if 'All users' in grant and obj['grants']['All users']['read']:
                self.items.append('s3-bucket-read-' + grant + '-' + obj['name'])
