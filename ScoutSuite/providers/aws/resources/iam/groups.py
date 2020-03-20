from ScoutSuite.providers.aws.resources.base import AWSResources


class Groups(AWSResources):
    async def fetch_all(self):
        raw_groups = await self.facade.iam.get_groups()
        for raw_group in raw_groups:
            name, resource = self._parse_group(raw_group)
            self[name] = resource

    def _parse_group(self, raw_group):
        if raw_group['GroupName'] in self:
            return

        raw_group['id'] = raw_group.pop('GroupId')
        raw_group['name'] = raw_group.pop('GroupName')
        raw_group['arn'] = raw_group.pop('Arn')
        raw_group['users'] = raw_group.pop('Users')
        return raw_group['id'], raw_group
