from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.aws.utils import format_arn


class Domains(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'route53'
        self.resource_type = 'domain'

    async def fetch_all(self):
        raw_domains = await self.facade.route53.get_domains(self.region)
        for raw_domain in raw_domains:
            id, domain = self._parse_domain(raw_domain)
            self[id] = domain

    def _parse_domain(self, raw_domain):
        domain_dict = {}
        domain_dict['id'] = get_non_provider_id(raw_domain.get('DomainName'))
        domain_dict['name'] = raw_domain.get('DomainName')
        domain_dict['auto_renew'] = raw_domain.get('AutoRenew')
        domain_dict['transfer_lock'] = raw_domain.get('TransferLock')
        domain_dict['expiry'] = raw_domain.get('Expiry')
        domain_dict['arn'] = format_arn(self.partition, self.service, self.region, self.facade.owner_id, domain_dict.get('id'), self.resource_type)
        return domain_dict['id'], domain_dict
