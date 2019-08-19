from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.aws.resources.iam.credentialreports import CredentialReports
from ScoutSuite.providers.aws.resources.iam.groups import Groups
from ScoutSuite.providers.aws.resources.iam.policies import Policies
from ScoutSuite.providers.aws.resources.iam.users import Users
from ScoutSuite.providers.aws.resources.iam.roles import Roles
from ScoutSuite.providers.aws.resources.iam.passwordpolicy import PasswordPolicy
from ScoutSuite.providers.aws.facade.base import AWSFacade


class IAM(AWSCompositeResources):
    _children = [
        (CredentialReports, 'credential_reports'),
        (Groups, 'groups'),
        (Policies, 'policies'),
        (Users, 'users'),
        (Roles, 'roles'),
        (PasswordPolicy, 'password_policy')
    ]

    def __init__(self, facade: AWSFacade):
        super(IAM, self).__init__(facade)
        self.service = 'iam'

    async def fetch_all(self, partition_name='aws', **kwargs):
        await self._fetch_children(self)

        # We do not want the report to count the password policies as resources, they aren't really resources.
        self['password_policy_count'] = 0

    async def finalize(self):
        # Update permissions for managed policies
        self['permissions'] = {}
        policies = [policy for policy in self['policies'].values()]
        self._parse_inline_policies_permissions('groups')
        self._parse_inline_policies_permissions('users')
        self._parse_inline_policies_permissions('roles')

        for policy in policies:
            policy_id = policy['id']
            if 'attached_to' in policy and len(policy['attached_to']) > 0:
                for entity_type in policy['attached_to']:
                    for entity in policy['attached_to'][entity_type]:
                        entity['id'] = self._get_id_for_resource(
                            entity_type, entity['name'])
                        entities = self[entity_type]
                        entities[entity['id']].setdefault('policies', [])
                        entities[entity['id']].setdefault('policies_counts', 0)
                        entities[entity['id']]['policies'].append(policy_id)
                        entities[entity['id']]['policies_counts'] += 1
                        self._parse_permissions(
                            policy_id, policy['PolicyDocument'], 'policies', entity_type, entity['id'])
            else:
                self._parse_permissions(
                    policy_id, policy['PolicyDocument'], 'policies', None, None)

    def _parse_inline_policies_permissions(self, resource_type):
        for resource_id in self[resource_type]:
            resource = self[resource_type][resource_id]
            if 'inline_policies' not in resource:
                continue

            for policy_id in resource['inline_policies']:
                policy = resource['inline_policies'][policy_id]
                self._parse_permissions(
                    policy_id, policy['PolicyDocument'], 'inline_policies', resource_type, resource_id)

    def _get_id_for_resource(self, iam_resource_type, resource_name):
        for resource_id in self[iam_resource_type]:
            if self[iam_resource_type][resource_id]['name'] == resource_name:
                return resource_id

    def _parse_permissions(self, policy_name, policy_document, policy_type, iam_resource_type, resource_name):
        # Enforce list of statements (Github issue #99)
        if type(policy_document['Statement']) != list:
            policy_document['Statement'] = [policy_document['Statement']]
        for statement in policy_document['Statement']:
            self._parse_statement(policy_name, statement,
                                  policy_type, iam_resource_type, resource_name)

    def _parse_statement(self, policy_name, statement, policy_type, iam_resource_type, resource_name):
        # Effect
        effect = str(statement['Effect'])
        # Action or NotAction
        action_string = 'Action' if 'Action' in statement else 'NotAction'
        if type(statement[action_string]) != list:
            statement[action_string] = [statement[action_string]]
        # Resource or NotResource
        resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
        if type(statement[resource_string]) != list:
            statement[resource_string] = [statement[resource_string]]
        # Condition
        condition = statement['Condition'] if 'Condition' in statement else None
        self['permissions'].setdefault(action_string, {})
        if iam_resource_type is None:
            return
        self._parse_actions(effect, action_string, statement[action_string], resource_string,
                            statement[resource_string], iam_resource_type, resource_name, policy_name, policy_type,
                            condition)

    def _parse_actions(self, effect, action_string, actions, resource_string, resources, iam_resource_type,
                       iam_resource_name, policy_name, policy_type, condition):
        for action in actions:
            self['permissions'][action_string].setdefault(action, {})
            self['permissions'][action_string][action].setdefault(
                iam_resource_type, {})
            self['permissions'][action_string][action][iam_resource_type].setdefault(
                effect, {})
            self['permissions'][action_string][action][iam_resource_type][effect].setdefault(
                iam_resource_name, {})
            self._parse_action(effect, action_string, action, resource_string, resources, iam_resource_type,
                               iam_resource_name, policy_name, policy_type, condition)

    def _parse_action(self, effect, action_string, action, resource_string, resources, iam_resource_type,
                      iam_resource_name, policy_name, policy_type, condition):
        for resource in resources:
            self._parse_resource(effect, action_string, action, resource_string, resource, iam_resource_type,
                                 iam_resource_name, policy_name, policy_type, condition)

    def _parse_resource(self, effect, action_string, action, resource_string, resource, iam_resource_type,
                        iam_resource_name, policy_name, policy_type, condition):
        self['permissions'][action_string][action][iam_resource_type][effect][iam_resource_name].setdefault(
            resource_string, {})
        self['permissions'][action_string][action][iam_resource_type][effect][iam_resource_name][resource_string].\
            setdefault(resource, {})
        self['permissions'][action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
            resource].setdefault(policy_type, {})
        self['permissions'][action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
            resource][policy_type].setdefault(policy_name, {})
        self['permissions'][action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
            resource][policy_type][policy_name].setdefault('condition', condition)
