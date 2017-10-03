# -*- coding: utf-8 -*-
"""
EFS-related classes and functions
"""
from opinel.utils.aws import get_name, handle_truncated_response

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# EFSRegionConfig
########################################

class EFSRegionConfig(RegionConfig):
    """
    EFS configuration for a single AWS region
    """

    def parse_file_system(self, global_params, region, file_system):
        """

        :param global_params:
        :param region:
        :param file_system:
        :return:
        """
        fs_id = file_system.pop('FileSystemId')
        file_system['name'] = file_system.pop('Name')
        # Get tags
        file_system['tags'] = handle_truncated_response(api_clients[region].describe_tags, {'FileSystemId': fs_id}, ['Tags'])['Tags']
        # Get mount targets
        mount_targets = handle_truncated_response(api_clients[region].describe_mount_targets, {'FileSystemId': fs_id}, ['MountTargets'])['MountTargets']
        file_system['mount_targets'] = {}
        for mt in mount_targets:
            mt_id = mt['MountTargetId']
            file_system['mount_targets'][mt_id] = mt
            # Get security groups
            file_system['mount_targets'][mt_id]['security_groups'] = api_clients[region].describe_mount_target_security_groups(MountTargetId = mt_id)['SecurityGroups']
        self.file_systems[fs_id] = file_system



########################################
# EFSConfig
########################################

class EFSConfig(RegionalServiceConfig):
    """
    EFS configuration for all AWS regions
    """

    region_config_class = EFSRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(EFSConfig, self).__init__(service_metadata, thread_config)
