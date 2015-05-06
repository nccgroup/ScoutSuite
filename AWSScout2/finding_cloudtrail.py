#!/usr/bin/env python2

from AWSScout2.finding import *

class CloudTrailFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'cloudtrail'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)

    def checkLoggingIsEnabled(self, key, obj):
        if obj['trails']:
            for trail in obj['trails']:
                if not obj['trails'][trail]['IsLogging']:
                    self.addItem(key)
        else:
            self.addItem(key)

    def checkGlobalServicesLoggingIsEnabled(self, key, obj):
        # h4ck: update the entity to fix the JS in the report
        self.entity = 'regions'
        enabledRegions = self.getGlobalServicesLoggingRegions(obj)
        if len(enabledRegions) < 1:
            for r in obj['regions']:
                if len(obj['regions'][r]['trails']):
                    self.addItem(r)

    def checkGlobalServicesLoggingIsNotDuplicated(self, key, obj):
        # h4ck: update the entity to fix the JS in the report
        self.entity = 'regions'
        # Do the analysis
        enabledRegions = self.getGlobalServicesLoggingRegions(obj)
        if len(enabledRegions) > 1:
            for r in enabledRegions:
                self.addItem(r)

    def getGlobalServicesLoggingRegions(self, cloudtrail_info):
        enabledRegions = []
        for r in cloudtrail_info['regions']:
            self.checkedNewItem()
            for t in cloudtrail_info['regions'][r]['trails']:
                if cloudtrail_info['regions'][r]['trails'][t]['IncludeGlobalServiceEvents']:
                    enabledRegions.append(r)
        return enabledRegions
