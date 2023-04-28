from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name

from ScoutSuite.providers.azure.utils import get_resource_group_name

class Instances(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
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
        if raw_instance.availability_set is not None:
            #Get the resource group and availability set if set
            try:
                instance_dict['availability_set'] = raw_instance.availability_set.id.split('/')[4] + ':' + raw_instance.availability_set.id.split('/')[8]
            except Exception as e:
                instance_dict['availability_set'] = raw_instance.availability_set.id
        else:
            instance_dict['availability_set'] = None
        if raw_instance.proximity_placement_group is not None:
            #Get the resource group and proximity placement group if set  
            try:
                instance_dict['proximity_placement_group'] = raw_instance.proximity_placement_group.id.split('/')[4] + ':' + raw_instance.proximity_placement_group.id.split('/')[8]
            except Exception as e:
                instance_dict['proximity_placement_group'] = raw_instance.proximity_placement_group.id
        else:
            instance_dict['proximity_placement_group'] = None
        instance_dict['additional_properties'] = list(raw_instance.additional_properties)
        instance_dict['location'] = raw_instance.location
        instance_dict['type'] = raw_instance.type
        instance_dict['resources'] = raw_instance.resources
        if raw_instance.tags is not None:
            instance_dict['tags'] = ["{}:{}".format(key, value) for key, value in  raw_instance.tags.items()]
        else:
            instance_dict['tags'] = []
        instance_dict['resource_group_name'] = get_resource_group_name(raw_instance.id)
        instance_dict['provisioning_state'] = raw_instance.provisioning_state
        if raw_instance.plan is not None:
            instance_dict['plan'] = raw_instance.plan.name
        else:
            instance_dict['plan'] = None
        instance_dict['identity'] = raw_instance.identity

        if raw_instance.additional_capabilities is not None:
            #Get all the enabled additional capabilities ignoring not set or empty values
            instance_dict['additional_capabilities'] = [additional_capability for additional_capability, value in raw_instance.additional_capabilities.__dict__.items() if (value and value is not None)]
        else:
            instance_dict['additional_capabilities'] = None
        instance_dict['license_type'] = raw_instance.license_type

        # TODO process and display the below
        instance_dict['hardware_profile'] = raw_instance.hardware_profile.vm_size
        
        # Handle VMs without diagnostics profile configured
        if raw_instance.diagnostics_profile is not None:
            instance_dict['diagnostics_profile'] = {'Boot Diagnostics': True if raw_instance.diagnostics_profile.boot_diagnostics.enabled else None}
        
        instance_dict['os_profile'] = {}
        if raw_instance.os_profile is not None:
            instance_dict['os_profile']['Administrator Username'] = raw_instance.os_profile.admin_username
            instance_dict['os_profile']['Allow Extension Operations'] = raw_instance.os_profile.allow_extension_operations
            instance_dict['os_profile']['Computer Name'] = raw_instance.os_profile.computer_name
            instance_dict['os_profile']['Custom Data'] = raw_instance.os_profile.custom_data
            instance_dict['os_profile']['Secrets'] = ''.join(raw_instance.os_profile.secrets)
            if raw_instance.os_profile.windows_configuration:
                instance_dict['os_profile']['Unnatended Content'] = raw_instance.os_profile.windows_configuration.additional_unattend_content
                instance_dict['os_profile']['Automatic Updates'] = raw_instance.os_profile.windows_configuration.enable_automatic_updates
                instance_dict['os_profile']['VM Agent Provision'] = raw_instance.os_profile.windows_configuration.provision_vm_agent
                instance_dict['os_profile']['Windows Remote Management'] = raw_instance.os_profile.windows_configuration.win_rm
            elif raw_instance.os_profile.linux_configuration:
                instance_dict['os_profile']['Disable Password Authentication'] = raw_instance.os_profile.linux_configuration.disable_password_authentication
                instance_dict['os_profile']['VM Agent Provision'] = raw_instance.os_profile.linux_configuration.provision_vm_agent

        if raw_instance.storage_profile is not None:
            instance_dict['storage_profile'] = {}
            instance_dict['storage_profile']['Publisher'] = raw_instance.storage_profile.image_reference.publisher
            instance_dict['storage_profile']['Release'] = raw_instance.storage_profile.image_reference.version
            instance_dict['storage_profile']['SKU'] = raw_instance.storage_profile.image_reference.sku
            instance_dict['storage_profile']['Offer'] = raw_instance.storage_profile.image_reference.offer
            instance_dict['storage_profile']['Exact Version'] = raw_instance.storage_profile.image_reference.exact_version
            instance_dict['storage_profile']['OS Disk Size (GB)'] = raw_instance.storage_profile.os_disk.disk_size_gb
            instance_dict['storage_profile']['OS Disk Name'] = raw_instance.storage_profile.os_disk.name
            instance_dict['storage_profile']['OS Disk VHD'] = raw_instance.storage_profile.os_disk.vhd
            if raw_instance.storage_profile.os_disk.managed_disk:
                instance_dict['storage_profile'][
                    'OS Managed Disk ID'] = raw_instance.storage_profile.os_disk.managed_disk.id.split('/')[-1]
                instance_dict['storage_profile'][
                    'OS Managed Disk Storage Account Type'] = raw_instance.storage_profile.os_disk.managed_disk.storage_account_type
            else:
                instance_dict['storage_profile']['OS Managed Disk ID'] = None
                instance_dict['storage_profile']['OS Managed Disk Storage Account Type'] = None
            if raw_instance.storage_profile.data_disks is not None and raw_instance.storage_profile.data_disks:
                instance_dict['storage_profile']['Data Disks'] = ["{} ({}GB)".format(disk.name, disk.disk_size_gb) for disk in raw_instance.storage_profile.data_disks]
        else:
            instance_dict['storage_profile'] = None

        instance_dict['network_interfaces'] = []
        for interface in raw_instance.network_profile.network_interfaces:
            instance_dict['network_interfaces'].append(get_non_provider_id(interface.id))

        instance_dict['extensions'] = await self.facade.virtualmachines.get_instance_extensions(
            subscription_id=self.subscription_id,
            instance_name=instance_dict['name'],
            resource_group=get_resource_group_name(raw_instance.id))

        return instance_dict['id'], instance_dict
