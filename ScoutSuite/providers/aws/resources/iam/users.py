from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Users(AWSResources):
    async def fetch_all(self):
        raw_users = await self.facade.iam.get_users()
        parsing_error_counter = 0
        for raw_user in raw_users:
            try:
                name, resource = self._parse_user(raw_user)

                if name in self:
                    continue

                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_user(self, raw_user):
        raw_user['id'] = raw_user.pop('UserId')
        raw_user['name'] = raw_user.pop('UserName')
        raw_user['arn'] = raw_user.pop('Arn')
        if (len(raw_user['tags']['Tags']) > 0):
            raw_user['Tags'] = raw_user['tags']['Tags']
        return raw_user['id'], raw_user
