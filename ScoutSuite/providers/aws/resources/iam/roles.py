from ScoutSuite.providers.aws.resources.base import AWSResources


class Roles(AWSResources):
    async def fetch_all(self):
        raw_roles = await self.facade.iam.get_roles()
        for raw_role in raw_roles:
            name, resource = self._parse_role(raw_role)
            self[name] = resource

    def _parse_role(self, raw_role):
        raw_role['id'] = raw_role.pop('RoleId')
        raw_role['name'] = raw_role.pop('RoleName')
        raw_role['arn'] = raw_role.pop('Arn')
        if 'Description' in raw_role:  raw_role.pop('Description')
        raw_role.pop('MaxSessionDuration')
        return raw_role['id'], raw_role
