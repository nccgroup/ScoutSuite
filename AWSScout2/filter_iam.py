#!/usr/bin/env python2

from AWSScout2.filter import *


class IamFilter(Filter):

    def __init__(self, description, entity, callback, callback_args):
        self.keyword_prefix = 'iam'
        Filter.__init__(self, description, entity, callback, callback_args)

    def HasNoMembers(self, key, obj):
        if len(obj['users']) == 0:
            self.addItem(obj['id'])
