from ScoutSuite.core.console import print_debug, print_exception
from ScoutSuite.utils import manage_dictionary

from ScoutSuite.core.utils import recurse


# 整个 ScoutSuite 工具的核心，该类实现了对所有规则的遍历和执行。
class ProcessingEngine:
    """

    """

    # 构造函数，接收一个ruleset作为参数
    def __init__(self, ruleset):
        # Organize rules by path
        # 将其按路径整理并储存于self.rules属性中。
        self.ruleset = ruleset
        self.rules = {}
        for filename in self.ruleset.rules:
            for rule in self.ruleset.rules[filename]:
                if not rule.enabled:
                    continue
                try:
                    manage_dictionary(self.rules, rule.path, [])
                    self.rules[rule.path].append(rule)
                except Exception as e:
                    print_exception(f'Failed to create rule {rule.filename}: {e}')

    # 遍历所有资源类型和该资源类型下的所有资源，在执行每个规则之前，将清理现有的发现。
    def run(self, cloud_provider, skip_dashboard=False):
        # Clean up existing findings
        for service in cloud_provider.services:
            cloud_provider.services[service][self.ruleset.rule_type] = {}

        # Process each rule
        for finding_path in self._filter_rules(self.rules, cloud_provider.service_list):
            for rule in self.rules[finding_path]:
                # 检查规则是否启用，如果未启用，则跳过规则。
                if not rule.enabled:  # or rule.service not in []: # TODO: handle this...
                    continue

                print_debug(f'Processing {rule.service} rule "{rule.description}" ({rule.filename})')
                finding_path = rule.path
                path = finding_path.split('.')
                service = path[0]
                manage_dictionary(cloud_provider.services[service], self.ruleset.rule_type, {})
                cloud_provider.services[service][self.ruleset.rule_type][rule.key] = {}
                cloud_provider.services[service][self.ruleset.rule_type][rule.key]['description'] = rule.description
                cloud_provider.services[service][self.ruleset.rule_type][rule.key]['path'] = rule.path
                for attr in ['level', 'id_suffix', 'class_suffix', 'display_path']:
                    if hasattr(rule, attr):
                        cloud_provider.services[service][self.ruleset.rule_type][rule.key][attr] = getattr(rule, attr)
                try:
                    setattr(rule, 'checked_items', 0)
                    # 构建查找路径并处理规则。为此，它使用了recurse()方法，在该方法中将检查资源以及子资源是否符合规则。
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['items'] = recurse(
                        cloud_provider.services, cloud_provider.services, path, [], rule, True)
                    if skip_dashboard:
                        continue
                    # 将发现的问题以规定的格式保存在CloudProvider对象的services属性中。
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['dashboard_name'] = \
                        rule.dashboard_name
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['checked_items'] = \
                        rule.checked_items
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['flagged_items'] = \
                        len(cloud_provider.services[service][self.ruleset.rule_type][rule.key]['items'])
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['service'] = rule.service
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['rationale'] = \
                        rule.rationale if hasattr(rule, 'rationale') else None
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['remediation'] = \
                        rule.remediation if hasattr(rule, 'remediation') else None
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['compliance'] = \
                        rule.compliance if hasattr(rule, 'compliance') else None
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['references'] = \
                        rule.references if hasattr(rule, 'references') else None
                except Exception as e:
                    print_exception(f'Failed to process rule defined in {rule.filename}: {e}')
                    # Fallback if process rule failed to ensure report creation and data dump still happen
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['checked_items'] = 0
                    cloud_provider.services[service][self.ruleset.rule_type][rule.key]['flagged_items'] = 0

    # ProcessingEngine类的一个静态方法。它的作用是根据services列表中的资源名称过滤规则，并返回一个过滤后的规则字典。
    @staticmethod
    def _filter_rules(rules, services):
        return {rule_name: rule for rule_name, rule in rules.items() if rule_name.split('.')[0] in services}
