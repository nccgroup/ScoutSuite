# -*- coding: utf-8 -*-

import json

from AWSScout2.utils import format_service_name


class Rule(object):

    def __init__(self, filename, rule_type, enabled, level, arg_values):
        self.filename = filename
        self.rule_type = rule_type
        self.enabled = bool(enabled)
        self.level = level
        self.args = arg_values


    def set_definition(self, rule_definitions, attributes = []):
        """
        Update every attribute of the rule by setting the argument values as necessary

        :param parameterized_input:
        :param arg_values:
        :param convert:
        :return:
        """
        string_definition = rule_definitions[self.filename].string_definition
        parameters = re.findall(r'(_ARG_([a-zA-Z0-9]+)_)', string_definition)
        for param in parameters:
            index = int(param[1])
            string_definition = string_definition.replace(param[0], self.args[index])
        definition = json.loads(string_definition)
        if len(attributes) == 0:
            attributes = [attr for attr in definition]
        for attr in attributes:
            if attr in definition:
                setattr(self, attr, definition[attr])
        if hasattr(self, 'path'):
            self.service = format_service_name(self.path.split('.')[0])
        if not hasattr(self, 'key'):
            setattr(self, 'key', self.filename)
        setattr(self, 'key', self.key.replace('.json', ''))
