#!/usr/bin/env python2

import json

from AWSScout2.finding import *

class S3Finding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 's3'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)


########################################
##### Finding callbacks
########################################

    def checkWorldWritableBucket(self, key, obj):
        for grant in obj['grants']:
            if 'All users' in grant:
                if obj['grants']['All users']['write']:
                    self.addItem(key)

    def checkWorldWritableBucketPerms(self, key, obj):
        for grant in obj['grants']:
            if 'All users' in grant:
                if obj['grants']['All users']['write_acp']:
                    self.addItem(key)


    def checkWorldReadableBucket(self, key, obj):
        for grant in obj['grants']:
            if 'All users' in grant and obj['grants']['All users']['read']:
                self.addItem(key)

    def checkLogging(self, key, obj):
        if obj['logging'] == 'Disabled':
            self.addItem(key)

    def checkWebhosting(self, key, obj):
        if obj['web_hosting'] == 'Enabled':
            self.addItem(key)

    def checkEncryption(self, key, obj):
        if 'keys' in obj:
            for k in obj['keys']:
                if 'encrypted' in obj['keys'][k] and not obj['keys'][k]['encrypted']:
                    # Folders cant' be encrypted
                    if not k.endswith('/'):
                        self.addItem(k, key)
                    else:
                        obj['keys'][k]['encrypted'] = 'N/A'

    def checkObjectsPermissions(self, key, obj):
        if 'keys' in obj:
            bucket_grants = obj['grants']
            for k in obj['keys']:
                object_grants = obj['keys'][k]['grants']
                if cmp(bucket_grants, object_grants) != 0:
                    self.addItem(k, key)

    def checkStaticWebsiteHosting(self, key, obj):
        if obj['web_hosting'] == 'Enabled':
            self.addItem(key)

    def checkIPOnlyCondition(self, key, obj):
        if 'policy' in obj:
            policy = json.loads(obj['policy'])
            statements = self.getList(policy, 'Statement')
            for s in statements:
                conditions = self.getList(s, 'Condition')
                if len(conditions) == 1:
                    c = conditions[0]
                    # If only IP address based condition
                    if s['Effect'] == 'Deny' and 'NotIpAddress' in c:
                        self.addItem(key)
                    elif s['Effect'] == 'Allow' and 'IpAddress' in c:
                        self.addItem(key)

    def checkOpenPolicy(self, key, obj):
        open_policy = False
        deny_condition = False
        if 'policy' in obj:
            policy = json.loads(obj['policy'])
            statements = self.getList(policy, 'Statement')
            for s in statements:
                conditions = self.getList(s, 'Condition')
                if len(conditions) == 0 and s['Effect'] == 'Allow':
                    principals = self.getList(s, 'Principal')
                    for p in principals:
                        if 'AWS' in p and p['AWS'] == '*':
                            actions = self.getList(s, 'Action')
                            for a in actions:
                                if a == self.callback_args[0]:
                                    open_policy = True
                elif s['Effect'] == 'Deny':
                    deny_condition = True
        if not deny_condition and open_policy:
            self.addItem(key)


########################################
##### Helpers
########################################

    def getList(self, obj, list_name):
        l = []
        if list_name in obj:
            res = obj[list_name]
            if type(res) != list:
                l.append(res)
            else:
                l = res
        return l
