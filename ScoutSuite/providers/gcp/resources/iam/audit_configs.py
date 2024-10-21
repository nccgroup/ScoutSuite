from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class AuditConfigs(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_configs = await self.facade.cloudresourcemanager.get_audit_configs(self.project_id)
        for raw_config in raw_configs:
            raw_config['name'] = raw_config['service']
            raw_config['id'] = raw_config['service']
            self[get_non_provider_id(raw_config['service'])] = raw_config
