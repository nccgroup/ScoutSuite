# -*- coding: utf-8 -*-

import json
import os

from opinel.utils.console import printDebug, printError, printException


class RuleDefinition(object):

    def __init__(self, file_name = None, rule_dirs = [], string_definition = None):
        self.file_name = file_name
        self.rule_dirs = rule_dirs
        self.rule_types = ['findings', 'filters']
        self.rules_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        if self.file_name:
            self.load()
        elif string_definition:
            self.string_definition = string_definition
            self.load_from_string_definition()
        else:
            printError('Error')


    def __str__(self):
        desription = getattr(self, 'description')
        dlen = len(desription)
        padding = (80 - dlen) / 2 if dlen < 80 else 0
        value = '-' * 80 + '\n' + ' ' * padding + ' %s' % getattr(self, 'description') + '\n' + '-' * 80 + '\n'
        quiet_list = ['descriptions', 'rule_dirs', 'rule_types', 'rules_data_path', 'string_definition']
        value += '\n'.join(('%s: %s') % (attr, str(getattr(self, attr))) for attr in vars(self) if attr not in quiet_list)
        value += '\n'
        return value


    def load(self):
        """
        Load the definition of the rule, searching in the specified rule dirs first, then in the built-in definitions

        :return:                        None
        """
        file_name_valid = False
        rule_type_valid = False
        # Look for a locally-defined rule
        for rule_dir in self.rule_dirs:
            file_path = os.path.join(rule_dir, self.file_name) if rule_dir else self.file_name
            if os.path.isfile(file_path):
                self.file_path = file_path
                file_name_valid = True
                break
        # Look for a built-in rule
        if not file_name_valid:
            for rule_type in self.rule_types:
                if self.file_name.startswith(rule_type):
                    self.file_path = os.path.join(self.rules_data_path, self.file_name)
                    rule_type_valid = True
                    file_name_valid = True
                    break
            if not rule_type_valid:
                for rule_type in self.rule_types:
                    self.file_path = os.path.join(self.rules_data_path, rule_type, self.file_name)
                    if os.path.isfile(self.file_path):
                        file_name_valid = True
                        break
            else:
                if os.path.isfile(self.file_path):
                    file_name_valid = True
        if not file_name_valid:
            printError('Error: could not find %s' % self.file_name)
        else:
            try:
                with open(self.file_path, 'rt') as f:
                    self.string_definition = f.read()
                    self.load_from_string_definition()
            except Exception as e:
                printException(e)
                printError('Failed to load rule defined in %s' % file_path)


    def load_from_string_definition(self):
        definition = json.loads(self.string_definition)
        for attr in definition:
            setattr(self, attr, definition[attr])
