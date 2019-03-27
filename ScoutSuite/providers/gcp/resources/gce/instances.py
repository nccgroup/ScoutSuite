from ScoutSuite.providers.gcp.resources.resources import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.gce.instance_disks import InstanceDisks

class Instances(GCPCompositeResources):
    _children = [ 
        (InstanceDisks, 'disks')
    ]

    def __init__(self, gcp_facade, project_id, zone):
        self.gcp_facade = gcp_facade
        self.project_id = project_id
        self.zone = zone

    async def fetch_all(self):
        raw_instances = await self.gcp_facade.gce.get_instances(self.project_id, self.zone)
        for raw_instance in raw_instances:
            name, instance = await self._parse_instance(raw_instance)
            self[name] = instance
  
    async def _parse_instance(self, raw_instance):
        instance_dict = {}
        instance_dict['id'] = self.get_non_provider_id(raw_instance['name'])
        instance_dict['project_id'] = self.project_id
        instance_dict['name'] = raw_instance['name']
        instance_dict['description'] = self._get_description(raw_instance)
        instance_dict['creation_timestamp'] = raw_instance['creationTimestamp']
        instance_dict['zone'] = raw_instance['zone'].split('/')[-1]
        instance_dict['tags'] = raw_instance['tags']
        instance_dict['status'] = raw_instance['status']
        instance_dict['zone_url_'] = raw_instance['zone']
        instance_dict['network_interfaces'] = raw_instance['networkInterfaces']
        instance_dict['service_accounts'] = raw_instance['serviceAccounts']
        instance_dict['deletion_protection_enabled'] = raw_instance['deletionProtection']
        instance_dict['block_project_ssh_keys_enabled'] = self._is_block_project_ssh_keys_enabled(raw_instance)
        instance_dict['oslogin_enabled'] = await self._is_oslogin_enabled(raw_instance)
        instance_dict['ip_forwarding_enabled'] = raw_instance['canIpForward']
        instance_dict['serial_port_enabled'] = self._is_serial_port_enabled(raw_instance)
        instance_dict['has_full_access_cloud_apis'] = self._has_full_access_to_all_cloud_apis(raw_instance)
        instance_dict['disks'] = InstanceDisks(raw_instance)
        return instance_dict['id'], instance_dict

    def _get_description(self, raw_instance):
        description = raw_instance.get('description')   
        return description if description else 'N/A'

    def _is_block_project_ssh_keys_enabled(self, raw_instance):
        metadata = self._metadata_to_dict(raw_instance['metadata'])
        return metadata.get('block-project-ssh-keys') == 'true'

    def _metadata_to_dict(self, metadata):
        return dict((item['key'], item['value']) for item in metadata['items']) if 'items' in metadata else {}

    async def _get_common_instance_metadata_dict(self):
        project = await self.gcp_facade.gce.get_project(self.project_id)
        return self._metadata_to_dict(project['commonInstanceMetadata'])

    async def _is_oslogin_enabled(self, raw_instance):
        instance_metadata = self._metadata_to_dict(raw_instance['metadata'])
        if instance_metadata.get('enable-oslogin') == 'FALSE':
            return False
        elif instance_metadata.get('enable-oslogin') == 'TRUE':
            return True
        project_metadata = await self._get_common_instance_metadata_dict()
        return project_metadata.get('enable-oslogin') == 'TRUE'

    def _is_serial_port_enabled(self, raw_instance):
        metadata = self._metadata_to_dict(raw_instance['metadata'])
        return metadata.get('serial-port-enable') == 'true'

    def _has_full_access_to_all_cloud_apis(self, raw_instance):
        full_access_scope = 'https://www.googleapis.com/auth/cloud-platform'
        return any(full_access_scope in service_account['scopes'] for service_account in raw_instance['serviceAccounts'])

