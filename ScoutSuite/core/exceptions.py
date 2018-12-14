# -*- coding: utf-8 -*-
"""
Exceptions handling
"""

from opinel.utils.console import printDebug

from ScoutSuite import EXCEPTIONS
from ScoutSuite.output.js import JavaScriptReaderWriter


class RuleExceptions(object):

    def __init__(self, profile, file_path=None, foobar=None):
        self.profile = profile
        self.file_path = file_path
        self.jsrw = JavaScriptReaderWriter(self.profile)
        self.exceptions = self.jsrw.load_from_file(config_type=EXCEPTIONS,
                                                   config_path=self.file_path,
                                                   first_line=True)

    def process(self, cloud_provider):
        for service in self.exceptions:
            for rule in self.exceptions[service]:
                filtered_items = []
                if rule not in cloud_provider.services[service]['findings']:
                    printDebug('Warning:: key error should not be happening')
                    continue
                for item in cloud_provider.services[service]['findings'][rule]['items']:
                    if item not in self.exceptions[service][rule]:
                        filtered_items.append(item)
                cloud_provider.services[service]['findings'][rule]['items'] = filtered_items
                cloud_provider.services[service]['findings'][rule]['flagged_items'] = \
                    len(cloud_provider.services[service]['findings'][rule]['items'])
