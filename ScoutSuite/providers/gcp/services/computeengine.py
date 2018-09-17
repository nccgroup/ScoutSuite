# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class ComputeEngineConfig(GCPBaseConfig):
    targets = (
        ('instances', 'Instances', 'list', {'project': 'project_placeholder', 'zone': 'europe-west1-b'}, False),
        ('snapshots', 'Snapshots', 'list', {'project': 'project_placeholder'}, False),
        ('networks', 'Networks', 'list', {'project': 'project_placeholder'}, False),
        ('firewalls', 'Firewalls', 'list', {'project': 'project_placeholder'}, False),
    )

    def __init__(self, thread_config):
        self.library_type = 'api_client_library'

        self.instances = {}
        self.instances_count = 0
        self.snapshots = {}
        self.snapshots_count = 0
        self.networks = {}
        self.networks_count = 0
        self.firewalls = {}
        self.firewalls_count = 0

        # TODO figure out why GCP returns errors when running with more then 1 thread (multithreading)
        super(ComputeEngineConfig, self).__init__(thread_config=1)

    def parse_instances(self, instance, params):
        instance_dict = {}
        instance_dict['id'] = self.get_non_provider_id(instance['name'])
        instance_dict['name'] = instance['name']
        instance_dict['description'] = instance['description']
        instance_dict['creation_timestamp'] = instance['creationTimestamp']
        instance_dict['tags'] = instance['tags']
        instance_dict['status'] = instance['status']
        instance_dict['zone_url_'] = instance['zone']
        instance_dict['network_interfaces'] = instance['networkInterfaces']
        instance_dict['service_accounts'] = instance['serviceAccounts']
        instance_dict['deletion_protection'] = 'Enabled' if instance['deletionProtection'] else 'Disabled'

        instance_dict['disks'] = {}
        for disk in instance['disks']:
            instance_dict['disks'][self.get_non_provider_id(disk['deviceName'])] = {
                'type': disk['type'],
                'mode': disk['mode'],
                'source_url': disk['source'],
                'source_device_name': disk['deviceName'],
                'bootable': disk['boot']
                }

        self.instances[instance_dict['id']] = instance_dict

    def parse_snapshots(self, snapshot, params):
        snapshot_dict = {}
        snapshot_dict['id'] = snapshot['id']
        snapshot_dict['name'] = snapshot['name']
        snapshot_dict['description'] = snapshot['description']
        snapshot_dict['creation_timestamp'] = snapshot['creationTimestamp']
        snapshot_dict['status'] = snapshot['status']
        snapshot_dict['source_disk_id'] = snapshot['sourceDiskId']
        snapshot_dict['source_disk_url'] = snapshot['sourceDisk']
        self.snapshots[snapshot_dict['id']] = snapshot_dict

    def parse_networks(self, network, params):
        network_dict = {}
        network_dict['id'] = network['id']
        network_dict['name'] = network['name']
        network_dict['description'] = network['description'] if 'description' in network else None
        network_dict['creation_timestamp'] = network['creationTimestamp']
        network_dict['network_url'] = network['selfLink']
        network_dict['subnetwork_urls'] = network['subnetworks']
        network_dict['auto_subnet'] = network['autoCreateSubnetworks']
        network_dict['routing_config'] = network['routingConfig']
        self.networks[network_dict['id']] = network_dict

    def parse_firewalls(self, firewall, params):
        firewall_dict = {}
        firewall_dict['id'] = firewall['id']
        firewall_dict['name'] = firewall['name']
        firewall_dict['descriptiong'] = firewall['description'] if 'description' in firewall else None
        firewall_dict['creation_timestamp'] = firewall['creationTimestamp']
        firewall_dict['network_url'] = firewall['network']
        firewall_dict['priority'] = firewall['priority']
        firewall_dict['source_ranges'] = firewall['sourceRanges']
        firewall_dict['allowed'] = firewall['allowed']
        firewall_dict['direction'] = firewall['direction']
        firewall_dict['disabled'] = firewall['disabled']
        self.firewalls[firewall_dict['id']] = firewall_dict
