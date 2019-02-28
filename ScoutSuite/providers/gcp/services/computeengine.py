# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class ComputeEngineConfig(GCPBaseConfig):
    targets = (
        ('instances', 'Instances', 'list', {'project': '{{project_placeholder}}', 'zone': '{{zone_placeholder}}'}, False),
        ('snapshots', 'Snapshots', 'list', {'project': '{{project_placeholder}}'}, False),
        ('networks', 'Networks', 'list', {'project': '{{project_placeholder}}'}, False),
        ('subnetworks', 'Subnetworks', 'list', {'project': '{{project_placeholder}}', 'region': '{{region_placeholder}}'}, False),
        ('firewalls', 'Firewalls', 'list', {'project': '{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):
        self.library_type = 'api_client_library'

        self.instances = {}
        self.instances_count = 0
        self.snapshots = {}
        self.snapshots_count = 0
        self.networks = {}
        self.networks_count = 0
        self.subnetworks = {}
        self.subnetworks_count = 0
        self.firewalls = {}
        self.firewalls_count = 0

        # TODO figure out why GCP returns errors when running with more then 1 thread (multithreading)
        super(ComputeEngineConfig, self).__init__(thread_config=1)

    # def get_regions(self, client, project):
    #     """
    #     Returns a list of all the regions. Uses an attribute to store the list in order to only run once.
    #     :param client:
    #     :param project:
    #     :return:
    #     """
    #     try:
    #         if self.regions:
    #             return self.regions
    #         else:
    #             regions_list = []
    #             regions = client.regions().list(project=project).execute()['items']
    #             for region in regions:
    #                 regions_list.append(region['name'])
    #             self.regions = regions_list
    #             return regions_list
    #     except HttpError as e:
    #         raise e
    #     except Exception as e:
    #         printException(e)
    #         return None
    #
    # def get_zones(self, client, project):
    #     """
    #     Returns a list of all the zones. Uses an attribute to store the list in order to only run once.
    #     :param client:
    #     :param project:
    #     :return:
    #     """
    #     try:
    #         if self.zones:
    #             return self.zones
    #         else:
    #             zones_list = []
    #             zones = client.zones().list(project=project).execute()['items']
    #             for zone in zones:
    #                 zones_list.append(zone['name'])
    #             self.zones = zones_list
    #             return zones_list
    #     except HttpError as e:
    #         raise e
    #     except Exception as e:
    #         printException(e)
    #         return None

    def parse_instances(self, instance, params):
        project_id = self._get_project_id(instance)

        self.api_client = params['api_client']

        instance_dict = {}
        instance_dict['id'] = self.get_non_provider_id(instance['name'])
        instance_dict['project_id'] = project_id
        instance_dict['name'] = instance['name']
        instance_dict['description'] = instance['description'] if 'description' in instance and instance['description'] else 'N/A'
        instance_dict['creation_timestamp'] = instance['creationTimestamp']
        instance_dict['zone'] = instance['zone'].split('/')[-1]
        instance_dict['tags'] = instance['tags']
        instance_dict['status'] = instance['status']
        instance_dict['zone_url_'] = instance['zone']
        instance_dict['network_interfaces'] = instance['networkInterfaces']
        instance_dict['service_accounts'] = instance['serviceAccounts']
        instance_dict['deletion_protection_enabled'] = instance['deletionProtection']
        instance_dict['block_project_ssh_keys_enabled'] = self._is_block_project_ssh_keys_enabled(instance)
        instance_dict['oslogin_enabled'] = self._is_oslogin_enabled(instance, project_id)
        instance_dict['ip_forwarding_enabled'] = instance['canIpForward']
        instance_dict['serial_port_enabled'] = self._is_serial_port_enabled(instance)
        instance_dict['has_full_access_cloud_apis'] = self._has_full_access_to_all_cloud_apis(instance)

        # TODO this should be done in it's own getter method and merged with instances during postprocessing
        instance_dict['disks'] = {}
        if 'disks' in instance:
            for disk in instance['disks']:
                instance_dict['disks'][self.get_non_provider_id(disk['deviceName'])] = {
                    'type': disk['type'],
                    'mode': disk['mode'],
                    'source_url': disk['source'],
                    'source_device_name': disk['deviceName'],
                    'bootable': disk['boot'],
                    'encrypted_with_csek': self._is_encrypted_with_csek(disk)
                }

        self.instances[instance_dict['id']] = instance_dict

    def parse_snapshots(self, snapshot, params):
        snapshot_dict = {}
        snapshot_dict['id'] = snapshot['id']
        snapshot_dict['name'] = snapshot['name']
        snapshot_dict['description'] = snapshot['description'] if 'description' in snapshot and snapshot['description'] else 'N/A'
        snapshot_dict['creation_timestamp'] = snapshot['creationTimestamp']
        snapshot_dict['status'] = snapshot['status']
        snapshot_dict['source_disk_id'] = snapshot['sourceDiskId']
        snapshot_dict['source_disk_url'] = snapshot['sourceDisk']
        self.snapshots[snapshot_dict['id']] = snapshot_dict

    def parse_networks(self, network, params):
        network_dict = {}
        network_dict['id'] = network['id']
        network_dict['project_id'] = network['selfLink'].split('/')[-4]
        network_dict['name'] = network['name']
        network_dict['description'] = network['description'] if 'description' in network and network['description'] else 'N/A'
        network_dict['creation_timestamp'] = network['creationTimestamp']
        network_dict['network_url'] = network['selfLink']
        network_dict['subnetwork_urls'] = network.get('subnetworks', None)
        network_dict['auto_subnet'] = network.get('autoCreateSubnetworks',  None)
        network_dict['routing_config'] = network['routingConfig']
        self.networks[network_dict['id']] = network_dict

    def parse_subnetworks(self, subnetwork, params):
        subnetwork_dict = {}
        subnetwork_dict['id'] = subnetwork['id']
        subnetwork_dict['project_id'] = subnetwork['selfLink'].split('/')[-5]
        subnetwork_dict['region'] = subnetwork['region'].split('/')[-1]
        subnetwork_dict['region'] = subnetwork['region'].split('/')[-1]
        subnetwork_dict['name'] = "%s-%s" % (subnetwork['name'], subnetwork_dict['region'])
        subnetwork_dict['subnetwork'] = subnetwork['network'].split('/')[-1]
        subnetwork_dict['gateway_address'] = subnetwork['gatewayAddress']
        subnetwork_dict['ip_range'] = subnetwork['ipCidrRange']
        subnetwork_dict['creation_timestamp'] = subnetwork['creationTimestamp']
        subnetwork_dict['private_ip_google_access'] = subnetwork['privateIpGoogleAccess']
        self.subnetworks[subnetwork_dict['id']] = subnetwork_dict

    def parse_firewalls(self, firewall, params):
        firewall_dict = {}
        firewall_dict['id'] = firewall['id']
        firewall_dict['project_id'] = firewall['selfLink'].split('/')[-4]
        firewall_dict['name'] = firewall['name']
        firewall_dict['description'] = firewall['description'] if \
            'description' in firewall and firewall['description'] else 'N/A'
        firewall_dict['creation_timestamp'] = firewall['creationTimestamp']
        firewall_dict['network'] = firewall['network'].split('/')[-1]
        firewall_dict['network_url'] = firewall['network']
        firewall_dict['priority'] = firewall['priority']
        firewall_dict['source_ranges'] = firewall['sourceRanges'] if 'sourceRanges' in firewall else []
        firewall_dict['source_tags'] = firewall['sourceTags'] if 'sourceTags' in firewall else []
        firewall_dict['target_tags'] = firewall['targetTags'] if 'targetTags' in firewall else []
        firewall_dict['direction'] = firewall['direction']
        firewall_dict['disabled'] = firewall['disabled']

        # Parse FW rules
        for direction in ['allowed', 'denied']:
            direction_string = '%s_traffic' % direction
            firewall_dict[direction_string] = {
                'tcp': [],
                'udp': [],
                'icmp': []
            }
            if direction in firewall:
                firewall_dict['action'] = direction
                for rule in firewall[direction]:
                    if rule['IPProtocol'] not in firewall_dict[direction_string]:
                        firewall_dict[direction_string][rule['IPProtocol']] = ['*']
                    else:
                        if rule['IPProtocol'] == 'all':
                            for protocol in firewall_dict[direction_string]:
                                firewall_dict[direction_string][protocol] = ['0-65535']
                            break
                        else:
                            if firewall_dict[direction_string][rule['IPProtocol']] != ['0-65535']:
                                if 'ports' in rule:
                                    firewall_dict[direction_string][rule['IPProtocol']] += rule['ports']
                                else:
                                    firewall_dict[direction_string][rule['IPProtocol']] = ['0-65535']

        self.firewalls[firewall_dict['id']] = firewall_dict

    def _get_project_id(self, instance):
        return instance['selfLink'].split('/')[-5]

    def _metadata_to_dict(self, metadata):
        return dict((item['key'], item['value']) for item in metadata['items']) if 'items' in metadata else {}

    def _is_block_project_ssh_keys_enabled(self, instance):
        metadata = self._metadata_to_dict(instance['metadata'])
        return metadata.get('block-project-ssh-keys') == 'true'

    def _get_common_instance_metadata_dict(self, project_id):
        project = self.api_client.projects().get(project=project_id).execute()
        return self._metadata_to_dict(project['commonInstanceMetadata'])

    def _is_oslogin_enabled(self, instance, project_id):
        instance_metadata = self._metadata_to_dict(instance['metadata'])
        if instance_metadata.get('enable-oslogin') == 'FALSE':
            return False
        elif instance_metadata.get('enable-oslogin') == 'TRUE':
            return True
        project_metadata = self._get_common_instance_metadata_dict(project_id)
        return project_metadata.get('enable-oslogin') == 'TRUE'

    def _is_serial_port_enabled(self, instance):
        metadata = self._metadata_to_dict(instance['metadata'])
        return metadata.get('serial-port-enable') == 'true'

    def _has_full_access_to_all_cloud_apis(self, instance):
        full_access_scope = 'https://www.googleapis.com/auth/cloud-platform'
        return any(full_access_scope in service_account['scopes'] for service_account in instance['serviceAccounts'])

    def _is_encrypted_with_csek(self, disk):
        return 'diskEncryptionKey' in disk and 'sha256' in disk['diskEncryptionKey'] and disk['diskEncryptionKey']['sha256'] != ''
