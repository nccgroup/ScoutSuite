# -*- coding: utf-8 -*-

from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from ScoutSuite.providers.aws.configs.vpc import VPCConfig



########################################
# EMRRegionConfig
########################################

class EMRRegionConfig(RegionConfig):
    """
    EMR configuration for a single AWS region
    """

    def parse_cluster(self, global_params, region, cluster):
        """
        Parse a single EMR cluster

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 EMR cluster
        """
        cluster_id = cluster['Id']
        cluster = api_clients[region].describe_cluster(ClusterId = cluster_id)['Cluster']
        cluster['id'] = cluster.pop('Id')
        cluster['name'] = cluster.pop('Name')
        vpc_id = 'TODO' # The EMR API won't disclose the VPC ID, so wait until all configs have been fetch and look up the VPC based on the subnet ID
        manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].clusters[cluster_id] = cluster


########################################
# EMRConfig
########################################

class EMRConfig(RegionalServiceConfig):
    """
    EMR configuration for all AWS regions
    """

    region_config_class = EMRRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(EMRConfig, self).__init__(service_metadata, thread_config)
