from ScoutSuite.providers.aws.resources.base import AWSResources


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
