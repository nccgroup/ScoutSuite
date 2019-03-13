from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.core.console import print_error, print_exception
from ScoutSuite.providers.utils import run_concurrently, get_non_provider_id
from ScoutSuite.providers.aws.utils import is_throttled


class IAMFacade(AWSBaseFacade):
    async def get_credential_reports(self):
        client = AWSFacadeUtils.get_client('iam', self.session)
        response = client.generate_credential_report()

        if response['State'] != 'COMPLETE':
            print_error('Failed to generate a credential report.')
            return []

        report = client.get_credential_report()['Content']

        # The report is a CSV string. The first row contains the name of each column. The next rows
        # each represent an individual account. This algorithm provides a simple initial parsing.
        lines = report.splitlines()
        keys = lines[0].decode('utf-8').split(',')

        credential_reports = []
        for line in lines[1:]:
            credential_report = {}
            values = line.decode('utf-8').split(',')
            for key, value in zip(keys, values):
                credential_report[key] = value

            credential_reports.append(credential_report)

        return credential_reports

    async def get_groups(self):
        groups = await AWSFacadeUtils.get_all_pages('iam', None, self.session, 'list_groups', 'Groups')
        for group in groups:
            group['Users'] = await self._fetch_group_users(group['GroupName'])
            policies = self._get_inline_policies('group', group['GroupId'], group['GroupName'])
            if len(policies):
                group['inline_policies'] = policies
        return groups

    async def _fetch_group_users(self, group_name):
        client =  AWSFacadeUtils.get_client('iam', self.session)
        fetched_users = client.get_group(GroupName=group_name)['Users']

        users = []
        for user in fetched_users:
            users.append(user['UserId'])
        return users

    def _get_inline_policies(self, iam_resource_type, resource_id, resource_name):
        client = AWSFacadeUtils.get_client('iam', self.session)
        get_policy_method = getattr(client, 'get_' + iam_resource_type + '_policy')
        fetched_policies = {}
        list_policy_method = getattr(client, 'list_' + iam_resource_type + '_policies')
        args = {iam_resource_type.title() + 'Name': resource_name}
        try:
            policy_names = list_policy_method(**args)['PolicyNames']
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                print_exception(e)
                return fetched_policies
        try:
            for policy_name in policy_names:
                args['PolicyName'] = policy_name
                policy_document = get_policy_method(**args)['PolicyDocument']
                policy_id = get_non_provider_id(policy_name)
                fetched_policies[policy_id] = {}
                fetched_policies[policy_id]['PolicyDocument'] = policy_document
                fetched_policies[policy_id]['name'] = policy_name
                # self._parse_permissions(policy_id, policy_document, 'inline_policies', iam_resource_type + 's', resource_id)
        except Exception as e:
            if is_throttled(e):
                raise e
            else:
                print_exception(e)
        return fetched_policies

    # def _parse_permissions(self, policy_name, policy_document, policy_type, iam_resource_type, resource_name):
    #     # Enforce list of statements (Github issue #99)
    #     if type(policy_document['Statement']) != list:
    #         policy_document['Statement'] = [policy_document['Statement']]
    #     for statement in policy_document['Statement']:
    #         self._parse_statement(policy_name, statement, policy_type, iam_resource_type, resource_name)

    # def _parse_statement(self, policy_name, statement, policy_type, iam_resource_type, resource_name):
    #     # Effect
    #     effect = str(statement['Effect'])
    #     # Action or NotAction
    #     action_string = 'Action' if 'Action' in statement else 'NotAction'
    #     if type(statement[action_string]) != list:
    #         statement[action_string] = [statement[action_string]]
    #     # Resource or NotResource
    #     resource_string = 'Resource' if 'Resource' in statement else 'NotResource'
    #     if type(statement[resource_string]) != list:
    #         statement[resource_string] = [statement[resource_string]]
    #     # Condition
    #     condition = statement['Condition'] if 'Condition' in statement else None
    #     if iam_resource_type is None:
    #         return

    #     self.__parse_actions(effect, action_string, statement[action_string], resource_string,
    #                          statement[resource_string], iam_resource_type, resource_name, policy_name, policy_type,
    #                          condition)

    # def _parse_action(self, effect, action_string, action, resource_string, resources, iam_resource_type, 
    #                     iam_resource_name, policy_name, policy_type, condition):
    #     for resource in resources:
    #         self.__parse_resource(effect, action_string, action, resource_string, resource, iam_resource_type,
    #                               iam_resource_name, policy_name, policy_type, condition)

    # def _parse_resource(self, effect, action_string, action, resource_string, resource, iam_resource_type,
    #                      iam_resource_name, policy_name, policy_type, condition):
    #     manage_dictionary(self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name],
    #                       resource_string, {})
    #     manage_dictionary(
    #         self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string],
    #         resource, {})
    #     manage_dictionary(
    #         self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
    #             resource], policy_type, {})
    #     manage_dictionary(
    #         self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
    #             resource][policy_type], policy_name, {})
    #     self.permissions[action_string][action][iam_resource_type][effect][iam_resource_name][resource_string][
    #         resource][policy_type][policy_name]['condition'] = condition