from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id

from ScoutSuite.providers.azure.utils import get_resource_group_name

class Instances(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Instances, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_instance in await self.facade.virtualmachines.get_instances(self.subscription_id):
            id, instance = await self._parse_instance(raw_instance)
            self[id] = instance

    async def _parse_instance(self, raw_instance):
        instance_dict = {}
        instance_dict['id'] = get_non_provider_id(raw_instance.id.lower())
        instance_dict['name'] = raw_instance.name
        instance_dict['vm_id'] = raw_instance.vm_id
        instance_dict['zones'] = raw_instance.zones
        instance_dict['instance_view'] = raw_instance.instance_view
        instance_dict['availability_set'] = raw_instance.availability_set
        instance_dict['proximity_placement_group'] = raw_instance.proximity_placement_group
        instance_dict['additional_properties'] = list(raw_instance.additional_properties)
        instance_dict['location'] = raw_instance.location
        instance_dict['type'] = raw_instance.type
        instance_dict['resources'] = raw_instance.resources
        instance_dict['tags'] = raw_instance.tags
        instance_dict['provisioning_state'] = raw_instance.provisioning_state
        instance_dict['plan'] = raw_instance.plan
        instance_dict['identity'] = raw_instance.identity
        instance_dict['additional_capabilities'] = raw_instance.additional_capabilities
        instance_dict['license_type'] = raw_instance.license_type

        # TODO process and display the below
        instance_dict['hardware_profile'] = raw_instance.hardware_profile
        instance_dict['diagnostics_profile'] = raw_instance.diagnostics_profile
        instance_dict['os_profile'] = raw_instance.os_profile
        instance_dict['storage_profile'] = raw_instance.storage_profile
        instance_dict['network_profile'] = raw_instance.network_profile

        # instance_dict['network_profile'] = raw_instance.network_profile
        instance_dict['network_interfaces'] = []
        for interface in raw_instance.network_profile.network_interfaces:
            instance_dict['network_interfaces'].append(get_non_provider_id(interface.id))

        instance_dict['extensions'] = await self.facade.virtualmachines.get_instance_extensions(
            subscription_id=self.subscription_id,
            instance_name=instance_dict['name'],
            resource_group=get_resource_group_name(raw_instance.id))

        return instance_dict['id'], instance_dict
