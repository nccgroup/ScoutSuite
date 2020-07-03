import json
import os

from ScoutSuite.core.console import print_error, print_exception


class RuleDefinition:

    def __init__(self, data_path, file_name=None, rule_dirs=None, string_definition=None):
        rule_dirs = [] if rule_dirs is None else rule_dirs
        self.rules_data_path = data_path
        self.file_name = file_name
        self.rule_dirs = rule_dirs
        self.rule_types = ['findings', 'filters']

        if self.file_name:
            self.load()
        elif string_definition:
            self.string_definition = string_definition
            self.load_from_string_definition()
        else:
            print_error('Error')

    def __str__(self):
        desription = getattr(self, 'description')
        dlen = len(desription)
        padding = (80 - dlen) // 2 if dlen < 80 else 0
        value = '-' * 80 + '\n' + ' ' * padding + ' %s' % getattr(self, 'description') + '\n' + '-' * 80 + '\n'
        quiet_list = ['descriptions', 'rule_dirs', 'rule_types', 'rules_data_path', 'string_definition']
        value += '\n'.join(
            '{}: {}'.format(attr, str(getattr(self, attr))) for attr in vars(self) if attr not in quiet_list)
        value += '\n'
        return value

    def load(self):
        """
        Load the definition of the rule, searching in the specified rule dirs first, then in the built-in definitions

        :return:                        None
        """
        file_name_valid = False
        rule_type_valid = False
        file_path = None
        # Look for a locally-defined rule
        for rule_dir in self.rule_dirs:
            try:
                file_path = os.path.join(rule_dir, self.file_name) if rule_dir else self.file_name
            except Exception as e:
                print_exception('Failed to load file {}: {}'.format(self.file_name, str(e)))
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
            print_error('Error: could not find %s' % self.file_name)
        else:
            try:
                with open(self.file_path) as f:
                    self.string_definition = f.read()
                    self.load_from_string_definition()
            except Exception as e:
                print_exception('Failed to load rule defined in {}: {}'.format(self.file_name, str(e)))

    def load_from_string_definition(self):
        try:
            definition = json.loads(self.string_definition)
            for attr in definition:
                setattr(self, attr, definition[attr])
        except Exception as e:
            print_exception('Failed to load string definition {}: {}'.format(self.string_definition, str(e)))
