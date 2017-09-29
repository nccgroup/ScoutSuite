# -*- coding: utf-8 -*-
"""
Exceptions handling
"""

import json

from AWSScout2 import EXCEPTIONS
from AWSScout2.output.js import JavaScriptReaderWriter

class RuleExceptions(object):

    def __init__(self, profile, file_path = None, foobar = None): 
        self.profile = profile
        self.file_path = file_path
        self.jsrw = JavaScriptReaderWriter(self.profile)
        self.exceptions = self.jsrw.load_from_file(config_type = EXCEPTIONS, config_path = self.file_path, first_line = True)

    def process(self, aws_config):
        for service in self.exceptions:
            for rule in self.exceptions[service]:
                filtered_items = []
                for item in aws_config['services'][service]['findings'][rule]['items']:
                    if item not in self.exceptions[service][rule]:
                        filtered_items.append(item)
                aws_config['services'][service]['findings'][rule]['items'] = filtered_items
                aws_config['services'][service]['findings'][rule]['flagged_items'] = len(aws_config['services'][service]['findings'][rule]['items'])
