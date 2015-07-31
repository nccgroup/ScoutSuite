#!/usr/bin/env python2

# Import Scout2 tools
from AWSScout2.finding import *

# Import stock packages
import json
import re

class S3Finding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 's3'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)


########################################
##### Finding callbacks
########################################

    def checkBucketACLs(self, key, obj):
        grantee = self.callback_args[0]
        grant = self.callback_args[1]
        if 'grantees' in obj and grantee in obj['grantees']:
            if obj['grantees'][grantee]['permissions'][grant] == True:
                self.addItem(key)

    def checkLogging(self, key, obj):
        if obj['logging'] == 'Disabled':
            self.addItem(key)

    def checkVersioning(self, key, obj):
        if obj['versioning_status'] == 'Disabled':
            self.addItem(key)

    def checkEncryption(self, key, obj):
        if 'keys' in obj:
            for k in obj['keys']:
                if 'ServerSideEncryption' in obj['keys'][k] and not obj['keys'][k]['ServerSideEncryption']:
                    # Folders cant' be encrypted
                    if not k.endswith('/'):
                        self.addItem(k, key)

    def checkObjectsPermissions(self, key, obj):
        if 'keys' in obj:
            bucket_grants = obj['grantees']
            for k in obj['keys']:
                if 'grantees' in obj['keys'][k]:
                    object_grants = obj['keys'][k]['grantees']
                    if cmp(bucket_grants, object_grants) != 0:
                        self.addItem(k, key)

    def checkStaticWebsiteHosting(self, key, obj):
        if 'web_hosting' in obj and obj['web_hosting'] == 'Enabled':
            self.addItem(key)

    def checkIPOnlyCondition(self, key, obj):
        if 'policy' in obj:
            policy = obj['policy']
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
        if 'policy' in obj:
            policy = obj['policy']
            statements = self.getList(policy, 'Statement')
            for s in statements:
                conditions = self.getList(s, 'Condition')
                if len(conditions) == 0 and s['Effect'] == 'Allow':
                    principals = self.getList(s, 'Principal')
                    for p in principals:
                        if 'AWS' in p and p['AWS'] == '*' or p == '*':
                            actions = self.getList(s, 'Action')
                            for a in actions:
                                if self.callback_args[0] != 's3:*' and re.match(self.callback_args[0], a):
                                    open_policy = True
                                elif a == self.callback_args[0]:
                                    open_policy = True
        if open_policy:
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
