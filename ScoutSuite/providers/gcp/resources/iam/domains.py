from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Domains(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_bindings = await self.facade.cloudresourcemanager.get_member_bindings(self.project_id)
        parsed_domains = self._parse_binding(raw_bindings)
        for domain_id in parsed_domains.keys():
            self[parsed_domains[domain_id]['id']] = parsed_domains[domain_id]

    def _parse_binding(self, raw_bindings):

        parsed_groups = {}
        for binding in raw_bindings:
            role = binding['role'].split('/')[-1]
            if 'members' in binding:
                for member in binding['members']:
                    member_type, entity = member.split(':')[:2]
                    if member_type == 'domain':
                        if entity not in parsed_groups.keys():
                            parsed_groups[entity] = {'id': get_non_provider_id(entity),
                                                    'name': entity,
                                                    'roles': [role]}
                        else:
                            parsed_groups[entity]['roles'].append(role)
        return parsed_groups
