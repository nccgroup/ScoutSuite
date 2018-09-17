# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo


class ComputeEngineConfig(GCPBaseConfig):
    targets = (
        # ('instances', 'Instances', 'list', {'project': 'project_placeholder', 'zone': ''}, False),
        ('snapshots', 'Snapshots', 'list', {'project': 'project_placeholder'}, False),
        # ('networks', 'Networks', 'list', {'project': 'project_placeholder'}, False),
        # ('firewalls', 'Firewalls', 'list', {'project': 'project_placeholder'}, False),
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

        super(ComputeEngineConfig, self).__init__(thread_config)

    def parse_instances(self, instance, params):

        instance_dict = {}

        instance_dict['id'] = self.get_non_provider_id(instance['name'])

        self.instances[instance_dict['id']] = instance_dict

    def parse_snapshots(self, snapshot, params):

        snapshot_dict = {}
        snapshot_dict['id'] = snapshot['id']
        snapshot_dict['name'] = snapshot['name']
        snapshot_dict['creation_timestamp'] = snapshot['creationTimestamp']
        snapshot_dict['description'] = snapshot['description']
        snapshot_dict['status'] = snapshot['status']
        snapshot_dict['source_disk_id'] = snapshot['sourceDiskId']
        snapshot_dict['source_disk'] = snapshot['sourceDisk']
        self.snapshots[snapshot_dict['id']] = snapshot_dict


    def parse_networks(self, network, params):

        network_dict = {}
        network_dict['id'] = network['id']


        self.networks[network_dict['id']] = network_dict

    def parse_firewalls(self, firewall, params):

        firewall_dict = {}
        firewall_dict['id'] = firewall['id']


        self.firewalls[firewall_dict['id']] = firewall_dict

