from ScoutSuite.providers.aws.resources.base import AWSResources


class Users(AWSResources):
    async def fetch_all(self):
        raw_users = await self.facade.iam.get_users()
        for raw_user in raw_users:
            name, resource = self._parse_user(raw_user)
              
            if name in self:
                continue

            self[name] = resource

    def _parse_user(self, raw_user):
        raw_user['id'] = raw_user.pop('UserId')
        raw_user['name'] = raw_user.pop('UserName')
        raw_user['arn'] = raw_user.pop('Arn')
        if (len(raw_user['tags']['Tags']) > 0):
            raw_user['Tags'] = raw_user['tags']['Tags']
        return raw_user['id'], raw_user
