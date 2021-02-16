from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade
from ScoutSuite.core.console import print_exception


class ApiKeys(AliyunResources):
    def __init__(self, facade: AliyunFacade, user):
        super().__init__(facade)
        self.user = user

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_user_api_key in await self.facade.ram.get_user_api_keys(username=self.user['name']):
            try:
                id, api_key = await self._parse_api_key(raw_user_api_key)
                self[id] = api_key
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    async def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = raw_api_key['AccessKeyId']
        api_key['creation_datetime'] = raw_api_key['CreateDate']
        api_key['status'] = raw_api_key['Status']

        last_usage = await self.facade.ram.get_user_api_key_last_usage(self.user['name'], api_key['id'])
        api_key['last_usage_datetime'] = last_usage if last_usage != 'N/A' else None

        return api_key['id'], api_key
