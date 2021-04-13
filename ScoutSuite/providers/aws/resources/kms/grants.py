from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class Grants(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, key_id: str):
        super().__init__(facade)
        self.region = region
        self.key_id = key_id
        self.partition = facade.partition
        self.service = 'kms'
        self.resource_type = 'grant'

    async def fetch_all(self):
        raw_grants = await self.facade.kms.get_grants(self.region, self.key_id)
        for raw_grant in raw_grants:
            id, grant = self._parse_grant(raw_grant)
            self[id] = grant

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
            'constraints': raw_grant.get('Constraints'),
            'arn': format_arn(self.partition, self.service, self.region, raw_grant.get('IssuingAccount').split(':')[4], raw_grant.get('GrantId'), self.resource_type) if ':' in raw_grant.get('IssuingAccount') else format_arn(self.partition, self.service, self.region, raw_grant.get('IssuingAccount'), raw_grant.get('GrantId'), self.resource_type)
        }
        return grant_dict['grant_id'], grant_dict
