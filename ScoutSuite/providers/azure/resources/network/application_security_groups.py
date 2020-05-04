from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class ApplicationSecurityGroups(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(ApplicationSecurityGroups, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_group in await self.facade.network.get_application_security_groups(self.subscription_id):
            id, application_security_group = self._parse_application_security_group(raw_group)
            self[id] = application_security_group

    def _parse_application_security_group(self, raw_application_security_group):
        application_security_group_dict = {}
        application_security_group_dict['id'] = get_non_provider_id(raw_application_security_group.id)
        application_security_group_dict['name'] = raw_application_security_group.name
        application_security_group_dict['type'] = raw_application_security_group.type
        application_security_group_dict['location'] = raw_application_security_group.location
        application_security_group_dict['tags'] = raw_application_security_group.tags
        application_security_group_dict['resource_guid'] = raw_application_security_group.resource_guid
        application_security_group_dict['provisioning_state'] = raw_application_security_group.provisioning_state
        application_security_group_dict['etag'] = raw_application_security_group.etag
        application_security_group_dict['network_interfaces'] = []  # this is filled in the base class
        return application_security_group_dict['id'], application_security_group_dict
