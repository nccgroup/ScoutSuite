import json
import os
import tempfile

from ScoutSuite.core.console import print_debug, print_error, prompt_yes_no, print_exception

from ScoutSuite.core.rule import Rule
from ScoutSuite.core.rule_definition import RuleDefinition

aws_ip_ranges_filename = 'ip-ranges.json'
ip_ranges_from_args = 'ip-ranges-from-args'


class Ruleset:
    """
    TODO

    :ivar rules:                        List of rules defined in the ruleset
    :ivar rule_definitions:             Definition of all rules found
    :ivar ??
    """

    def __init__(self,
                 cloud_provider,
                 environment_name='default',
                 filename=None,
                 name=None,
                 rules_dir=None,
                 rule_type='findings',
                 ip_ranges=None,
                 account_id=None,
                 ruleset_generator=False):
        rules_dir = [] if rules_dir is None else rules_dir
        ip_ranges = [] if ip_ranges is None else ip_ranges

        self.rules_data_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))) + '/providers/%s/rules' % cloud_provider

        self.environment_name = environment_name
        self.rule_type = rule_type
        # Ruleset filename
        self.filename = self.find_file(filename)
        if not self.filename:
            self.search_ruleset(environment_name)
        print_debug('Loading ruleset %s' % self.filename)
        self.name = os.path.basename(self.filename).replace('.json', '') if not name else name
        self.load(self.rule_type)
        self.shared_init(ruleset_generator, rules_dir, account_id, ip_ranges)

    def to_string(self):
        return str(vars(self))

    def shared_init(self, ruleset_generator, rule_dirs, account_id, ip_ranges):

        # Load rule definitions
        if not hasattr(self, 'rule_definitions'):
            self.load_rule_definitions(ruleset_generator, rule_dirs)

        # Prepare the rules
        params = {'account_id': account_id}
        if ruleset_generator:
            self.prepare_rules(attributes=['description', 'key', 'rationale'], params=params)
        else:
            self.prepare_rules(ip_ranges=ip_ranges, params=params)

    def load(self, rule_type, quiet=False):
        """
        Open a JSON file defining a ruleset and load it into a Ruleset object

        :param rule_type:           TODO
        :param quiet:               TODO
        :return:
        """
        if self.filename and os.path.exists(self.filename):
            try:
                with open(self.filename) as f:
                    ruleset = json.load(f)
                    self.about = ruleset['about'] if 'about' in ruleset else ''
                    self.rules = {}
                    for filename in ruleset['rules']:
                        self.rules[filename] = []
                        for rule in ruleset['rules'][filename]:
                            self.handle_rule_versions(filename, rule_type, rule)
            except Exception as e:
                print_exception(f'Ruleset file {self.filename} contains malformed JSON: {e}')
                self.rules = []
                self.about = ''
        else:
            self.rules = []
            if not quiet:
                print_error('Error: the file %s does not exist.' % self.filename)

    def load_rules(self, file, rule_type):
        file.seek(0)
        ruleset = json.load(file)
        self.about = ruleset['about']
        self.rules = {}
        for filename in ruleset['rules']:
            self.rules[filename] = []
            for rule in ruleset['rules'][filename]:
                self.handle_rule_versions(filename, rule_type, rule)

    def handle_rule_versions(self, filename, rule_type, rule):
        """
        For each version of a rule found in the ruleset, append a new Rule object
        """
        if 'versions' in rule:
            versions = rule.pop('versions')
            for version_key_suffix in versions:
                version = versions[version_key_suffix]
                version['key_suffix'] = version_key_suffix
                tmp_rule = dict(rule, **version)
                self.rules[filename].append(Rule(self.rules_data_path, filename, rule_type, tmp_rule))
        else:
            self.rules[filename].append(Rule(self.rules_data_path, filename, rule_type, rule))

    def prepare_rules(self, attributes=None, ip_ranges=None, params=None):
        """
        Update the ruleset's rules by duplicating fields as required by the HTML ruleset generator

        :return:
        """
        attributes = [] if attributes is None else attributes
        ip_ranges = [] if ip_ranges is None else ip_ranges
        params = {} if params is None else params
        for filename in self.rule_definitions:
            if filename in self.rules:
                for rule in self.rules[filename]:
                    rule.set_definition(self.rule_definitions, attributes, ip_ranges, params)
            else:
                self.rules[filename] = []
                new_rule = Rule(self.rules_data_path, filename, self.rule_type, {'enabled': False, 'level': 'danger'})
                new_rule.set_definition(self.rule_definitions, attributes, ip_ranges, params)
                self.rules[filename].append(new_rule)

    def load_rule_definitions(self, ruleset_generator=False, rule_dirs=None):
        """
        Load definition of rules declared in the ruleset

        :param ruleset_generator:
        :param rule_dirs:
        :return:
        """
        rule_dirs = [] if rule_dirs is None else rule_dirs

        # Load rules from JSON files
        self.rule_definitions = {}
        for rule_filename in self.rules:
            for rule in self.rules[rule_filename]:
                if not rule.enabled and not ruleset_generator:
                    continue
            self.rule_definitions[os.path.basename(rule_filename)] = RuleDefinition(self.rules_data_path,
                                                                                    rule_filename,
                                                                                    rule_dirs=rule_dirs)
        # In case of the ruleset generator, list all available built-in rules
        if ruleset_generator:
            rule_dirs.append(self.rules_data_path + '/findings')
            rule_filenames = []
            for rule_dir in rule_dirs:
                rule_filenames += [f for f in os.listdir(rule_dir) if os.path.isfile(os.path.join(rule_dir, f))]
            for rule_filename in rule_filenames:
                if rule_filename not in self.rule_definitions:
                    self.rule_definitions[os.path.basename(rule_filename)] = RuleDefinition(self.rules_data_path,
                                                                                            rule_filename)

    def search_ruleset(self, environment_name, no_prompt=False):
        """

        :param environment_name:
        :param no_prompt:
        :return:
        """
        ruleset_found = False
        if environment_name != 'default':
            ruleset_file_name = 'ruleset-%s.json' % environment_name
            ruleset_file_path = os.path.join(self.rules_data_path, 'rulesets/%s' % ruleset_file_name)
            if os.path.exists(ruleset_file_path):
                if no_prompt or prompt_yes_no(
                        "A ruleset whose name matches your environment name was found in %s. "
                        "Would you like to use it instead of the default one" % ruleset_file_name):
                    ruleset_found = True
                    self.filename = ruleset_file_path
        if not ruleset_found:
            self.filename = os.path.join(self.rules_data_path, 'rulesets/default.json')

    def find_file(self, filename, filetype='rulesets'):
        """

        :param filename:
        :param filetype:
        :return:
        """
        if filename and not os.path.isfile(filename):
            # Not a valid relative / absolute path, check Scout's data under findings/ or filters/
            if not filename.startswith('findings/') and not filename.startswith('filters/'):
                filename = f'{filetype}/{filename}'
            if not os.path.isfile(filename):
                filename = os.path.join(self.rules_data_path, filename)
            if not os.path.isfile(filename) and not filename.endswith('.json'):
                filename = self.find_file('%s.json' % filename, filetype)
        return filename


class TmpRuleset(Ruleset):

    def __init__(self, cloud_provider, rule_dirs=None, rule_filename=None, rule_args=None, rule_level='danger'):
        super().__init__(cloud_provider)
        rule_dirs = [] if rule_dirs is None else rule_dirs
        rule_args = [] if rule_args is None else rule_args
        self.rule_type = 'findings'
        tmp_ruleset = {'rules': {}, 'about': 'Temporary, single-rule ruleset.'}
        tmp_ruleset['rules'][rule_filename] = []
        rule = {'enabled': True, 'level': rule_level}
        if len(rule_args):
            rule['args'] = rule_args
        tmp_ruleset['rules'][rule_filename].append(rule)
        tmp_ruleset_file = tempfile.TemporaryFile('w+t')
        tmp_ruleset_file.write(json.dumps(tmp_ruleset))

        self.rules_data_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))) + '/providers/%s/rules' % cloud_provider

        self.load_rules(file=tmp_ruleset_file, rule_type='findings')

        self.shared_init(False, rule_dirs, '', [])
