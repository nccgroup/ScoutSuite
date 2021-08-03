from ScoutSuite.providers.aws.resources.base import AWSResources


class OrganizationalUnits(AWSResources):
    async def fetch_all(self):
        raw_units = await self.facade.organizations.collect_ous()
        for raw_unit in raw_units:
            name, resource = self._parse_unit(raw_unit)
            self[name] = resource

    def _parse_unit(self, raw_unit):
        unit = {}
        unit["name"] = raw_unit

        return unit["name"], unit
