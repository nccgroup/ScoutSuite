#!/usr/bin/env python2

from AWSScout2.finding import *

class S3Finding(Finding):

    def __init__(self, description, name, entity, callback, callback_args, idprefix, level):
        self.keyword_prefix = 's3'
        Finding.__init__(self, description, name, entity, callback, callback_args, idprefix, level)

    def checkWorldWritableBucket(self, key, obj):
        for grant in obj['grants']:
            if 'All users' in grant:
                if obj['grants']['All users']['write']:
                    self.items.append('s3-bucket-write-' + grant + '-' + key)
                    self.macro_items.append(key)
                if obj['grants']['All users']['write_acp']:
                    self.items.append('s3-bucket-write_acp-' + grant + '-' + key)
                    self.macro_items.append(key)

    def checkWorldReadableBucket(self, key, obj):
        for grant in obj['grants']:
            if 'All users' in grant and obj['grants']['All users']['read']:
                self.items.append('s3-bucket-read-' + grant + '-' + key)
                self.macro_items.append(key)
