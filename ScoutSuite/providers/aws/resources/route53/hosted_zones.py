from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class HostedZones(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(HostedZones, self).__init__(facade)
        self.region = region

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
