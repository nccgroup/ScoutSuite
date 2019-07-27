from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Route53Domains(AWSResources):
    async def fetch_all(self):
        raw_domains = await self.facade.route53.get_domains()
        for raw_domain in raw_domains:
            id, domain = self._parse_domain(raw_domain)
            self[id] = domain

    def _parse_domain(self, raw_domain):
        domain_id = get_non_provider_id(raw_domain['DomainName'])
        raw_domain['name'] = raw_domain.pop('DomainName')
        return domain_id, raw_domain


class Route53HostedZones(AWSResources):
    async def fetch_all(self):
        raw_hosted_zones = await self.facade.route53.get_hosted_zones()
        for raw_hosted_zone in raw_hosted_zones:
            hosted_zone_id, hosted_zone = await self._parse_hosted_zone(raw_hosted_zone)
            self[hosted_zone_id] = hosted_zone

    async def _parse_hosted_zone(self, raw_hosted_zone):
        hosted_zone_id = raw_hosted_zone.pop('Id')
        raw_hosted_zone['name'] = raw_hosted_zone.pop('Name')
        raw_hosted_zone['id'] = hosted_zone_id
        resource_records = await self.facade.route53.get_resource_records(hosted_zone_id)
        raw_hosted_zone['ResourceRecordSets'] = resource_records
        return hosted_zone_id, raw_hosted_zone


class Route53(AWSCompositeResources):
    _children = [
        (Route53Domains, 'domains'),
        (Route53HostedZones, 'hosted_zones')
    ]

    def __init__(self, facade: AWSFacade):
        super(Route53, self).__init__(facade)
        self.service = 'route53'

    async def fetch_all(self, regions=None, partition_name='aws'):
        await self._fetch_children(self)
