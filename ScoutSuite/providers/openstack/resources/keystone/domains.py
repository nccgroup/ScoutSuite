from ScoutSuite.providers.openstack.resources.base import OpenstackResources


class Domains(OpenstackResources):
    async def fetch_all(self):
        raw_domains = await self.facade.keystone.get_domains()
        for raw_domain in raw_domains:
            id, domain = self._parse_domain(raw_domain)
            if id in self:
                continue

            self[id] = domain

    def _parse_domain(self, raw_domain):
        domain_dict = {}
        domain_dict['id'] = raw_domain.id
        domain_dict['name'] = raw_domain.name
        domain_dict['description'] = raw_domain.description
        domain_dict['enabled'] = raw_domain.is_enabled
        return domain_dict['id'], domain_dict