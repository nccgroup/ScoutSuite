#!/usr/bin/env python

from AWSScout2.finding import *

import datetime
import dateutil.parser
import re

class S3Finding(Finding):

    def __init__(self, description, name, entity, callback, callback_args, idprefix, level):
        self.keyword_prefix = 's3'
        Finding.__init__(self, description, name, entity, callback, callback_args, idprefix, level)

    def checkWorldWritableBucket(self, obj):
        for grant in obj['grants']:
            if 'All users' in grant:
                if obj['grants']['All users']['write']:
                    self.items.append('s3-bucket-write-' + grant + '-' + obj['name'])
                if obj['grants']['All users']['write_acp']:
                    self.items.append('s3-bucket-write_acp-' + grant + '-' + obj['name'])
                    self.macro_items.append(obj['name'])

    def checkWorldReadableBucket(self, obj):
        for grant in obj['grants']:
            if 'All users' in grant and obj['grants']['All users']['read']:
                self.items.append('s3-bucket-read-' + grant + '-' + obj['name'])
                self.macro_items.append(obj['name'])
