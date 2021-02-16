from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Grants(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, key_id: str):
        super().__init__(facade)
        self.region = region
        self.key_id = key_id

    async def fetch_all(self):
        raw_grants = await self.facade.kms.get_grants(self.region, self.key_id)
        parsing_error_counter = 0
        for raw_grant in raw_grants:
            try:
                id, grant = self._parse_grant(raw_grant)
                self[id] = grant
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_grant(self, raw_grant):
        grant_dict = {
            'key_id': raw_grant.get('KeyId'),
            'grant_id': raw_grant.get('GrantId'),
            'name': raw_grant.get('Name'),
            'create_date': raw_grant.get('CreationDate'),
            'grantee_principal': raw_grant.get('GranteePrincipal'),
            'retiring_principal': raw_grant.get('ReitirngPrincipal'),
            'issuing_account': raw_grant.get('IssuingAccount'),
            'operations': raw_grant.get('Operations'),
            'constraints': raw_grant.get('Constraints')
        }
        return grant_dict['grant_id'], grant_dict
