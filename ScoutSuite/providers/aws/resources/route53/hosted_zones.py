from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import format_arn


class HostedZones(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'route53'
        self.resource_type = 'hosted-zone'

    async def fetch_all(self):
        raw_hosted_zones = await self.facade.route53.get_hosted_zones()
        for raw_hosted_zone in raw_hosted_zones:
            hosted_zone_id, hosted_zone = await self._parse_hosted_zone(raw_hosted_zone)
            self[hosted_zone_id] = hosted_zone

    async def _parse_hosted_zone(self, raw_hosted_zone):
        hosted_zone_dict = {}
        hosted_zone_dict['id'] = raw_hosted_zone.get('Id')
        hosted_zone_dict['name'] = raw_hosted_zone.get('Name')
        hosted_zone_dict['caller_reference'] = raw_hosted_zone.get('CallerReference')
        hosted_zone_dict['config'] = raw_hosted_zone.get('Config')
        hosted_zone_dict['resource_record_sets'] = await self.facade.route53.get_resource_records(hosted_zone_dict['id'])
        hosted_zone_dict['resource_record_set_count'] = raw_hosted_zone.get('ResourceRecordSetCount')
        hosted_zone_dict['arn'] = format_arn(self.partition,  self.service, self.region, '', raw_hosted_zone.get('Id'), self.resource_type)
        return hosted_zone_dict['id'], hosted_zone_dict
