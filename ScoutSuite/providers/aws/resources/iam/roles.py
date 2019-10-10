from ScoutSuite.providers.aws.resources.base import AWSResources


class Roles(AWSResources):
    async def fetch_all(self):
        raw_roles = await self.facade.iam.get_roles()
        for raw_role in raw_roles:
            name, resource = self._parse_role(raw_role)
            self[name] = resource

    def _parse_role(self, raw_role):
        role_dict = {}
        role_dict['id'] = raw_role.get('RoleId')
        role_dict['name'] = raw_role.get('RoleName')
        role_dict['arn'] = raw_role.get('Arn')
        role_dict['description'] = raw_role.get('Description')
        role_dict['path'] = raw_role.get('Path')
        role_dict['create_date'] = raw_role.get('CreateDate')
        role_dict['max_session_duration'] = raw_role.get('MaxSessionDuration')
        role_dict['instance_profiles'] = raw_role.get('instance_profiles')
        role_dict['instances_count'] = raw_role.get('instances_count')
        role_dict['inline_policies'] = raw_role.get('inline_policies')
        role_dict['inline_policies_count'] = raw_role.get('inline_policies_count')
        role_dict['assume_role_policy'] = raw_role.get('assume_role_policy')
        return role_dict['id'], role_dict
