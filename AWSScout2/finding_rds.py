#!/usr/bin/env python2

from AWSScout2.finding import *

class RdsFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'rds'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)

    def checkInternetAccessible(self, key, obj):
        for ip_range in obj['ip_ranges']:
            if ip_range == '0.0.0.0/0':
                self.addItem(obj['name'])
