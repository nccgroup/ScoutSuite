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

    def checkMultiAZ(self, key, obj):
        if not obj['multi_az']:
            self.addItem(obj['id'])

    def checkAutoUpgrade(self, key, obj):
        if not obj['auto_minor_version_upgrade']:
            self.addItem(obj['id'])

    def checkPostgresCreationDate(self, key, obj):
        if (obj['engine'] == 'postgres'):
            if self.wasCreatedBefore(key, obj):
                self.addItem(obj['id'])
