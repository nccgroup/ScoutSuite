from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.gce.instance_disks import InstanceDisks
from ScoutSuite.providers.utils import get_non_provider_id


class Instances(GCPCompositeResources):
    _children = [
        (InstanceDisks, 'disks')
    ]

    def __init__(self, facade: GCPFacade, project_id: str, zone: str):
        super().__init__(facade)
        self.project_id = project_id
        self.zone = zone

    async def fetch_all(self):
        raw_instances = await self.facade.gce.get_instances(self.project_id, self.zone)
        for raw_instance in raw_instances:
            instance_id, instance = self._parse_instance(raw_instance)
            self[instance_id] = instance
            self[instance_id]['disks'].fetch_all()

    def _parse_instance(self, raw_instance):
        instance_dict = {}
        instance_dict['id'] = get_non_provider_id(raw_instance['name'])
        instance_dict['project_id'] = self.project_id
        instance_dict['name'] = raw_instance['name']
        instance_dict['description'] = self._get_description(raw_instance)
        instance_dict['creation_timestamp'] = raw_instance['creationTimestamp']
        instance_dict['zone'] = raw_instance['zone'].split('/')[-1]
        instance_dict['tags'] = raw_instance['tags']
        instance_dict['status'] = raw_instance['status']
        instance_dict['zone_url_'] = raw_instance['zone']
        instance_dict['network_interfaces'] = raw_instance['networkInterfaces']
        instance_dict['deletion_protection_enabled'] = raw_instance['deletionProtection']
        instance_dict['block_project_ssh_keys_enabled'] = self._is_block_project_ssh_keys_enabled(raw_instance)
        instance_dict['oslogin_enabled'] = self._is_oslogin_enabled(raw_instance)
        instance_dict['ip_forwarding_enabled'] = raw_instance.get("canIpForward", False)
        instance_dict['serial_port_enabled'] = self._is_serial_port_enabled(raw_instance)
        instance_dict['disks'] = InstanceDisks(self.facade, raw_instance)
        instance_dict['public_ip_addresses'] = self._public_ip_adresses(raw_instance)

        if 'serviceAccounts' in raw_instance and raw_instance.get('serviceAccounts'):
            instance_dict['service_account'] = raw_instance.get('serviceAccounts')[0].get('email')
            instance_dict['access_scopes'] = raw_instance.get('serviceAccounts')[0].get('scopes')
            instance_dict['default_service_account'] = \
                self._is_default_service_account(instance_dict['service_account'])
            instance_dict['full_access_apis'] = self._allow_full_access_to_all_cloud_api(raw_instance)
        else:
            instance_dict['service_account'] = None
            instance_dict['access_scopes'] = None
            instance_dict['default_service_account'] = False
            instance_dict['full_access_apis'] = False

        if 'shieldedInstanceConfig' in raw_instance:
            instance_dict['shielded_enable'] = self._shielded_vm_enabled(raw_instance)
        else:
            instance_dict['shielded_enable'] = False

        return instance_dict['id'], instance_dict

    def _get_description(self, raw_instance):
        description = raw_instance.get('description')
        return description if description else 'N/A'

    def _is_block_project_ssh_keys_enabled(self, raw_instance):
        return raw_instance['metadata'].get('block-project-ssh-keys') == 'true'

    def _is_oslogin_enabled(self, raw_instance):
        instance_logging_enabled = raw_instance['metadata'].get('enable-oslogin')
        project_logging_enabled = raw_instance['commonInstanceMetadata'].get('enable-oslogin')
        return instance_logging_enabled == 'TRUE' \
               or instance_logging_enabled is None and project_logging_enabled == 'TRUE'

    def _is_serial_port_enabled(self, raw_instance):
        return raw_instance['metadata'].get('serial-port-enable') == 'true'

    def _is_default_service_account(self, service_account: str):
        if '-compute@developer.gserviceaccount.com' in service_account:
            return True
        return False

    def _allow_full_access_to_all_cloud_api(self, raw_instance):
        if '-compute@developer.gserviceaccount.com' in raw_instance.get('serviceAccounts')[0].get('email'):
            for scope in raw_instance.get('serviceAccounts')[0].get('scopes'):
                if scope == 'https://www.googleapis.com/auth/cloud-platform':
                    return True
        return False

    def _shielded_vm_enabled(self, raw_instance):
        vtpm = raw_instance['shieldedInstanceConfig'].get('enableVtpm', False)
        integrity_monitoring = raw_instance['shieldedInstanceConfig'].get('enableIntegrityMonitoring', False)
        secure_boot = raw_instance['shieldedInstanceConfig'].get('enableSecureBoot', False)
        return vtpm and integrity_monitoring and secure_boot

    def _public_ip_adresses(self, raw_instance):
        for network in raw_instance['networkInterfaces']:
            access_configs = network.get('accessConfigs', None)
            if access_configs:
                return True
        return False
