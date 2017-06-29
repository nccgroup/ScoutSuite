# -*- coding: utf-8 -*-

from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.utils import ec2_classic



########################################
# EMRRegionConfig
########################################

class EMRRegionConfig(RegionConfig):
    """
    EMR configuration for a single AWS region

    :ivar vpcs:                         Dictionary of VPCs [id]
    :ivar clusters_count:               Number of clusters in the region
    """

    def __init__(self):
        self.vpcs = {}
        self.clusters_count = 0


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
        manage_dictionary(self.vpcs, vpc_id, EMRVPCConfig())
        self.vpcs[vpc_id].clusters[cluster_id] = cluster


########################################
# EMRConfig
########################################

class EMRConfig(RegionalServiceConfig):
    """
    EMR configuration for all AWS regions

    :cvar targets:                      Tuple with all EMR resource names that may be fetched
    :cvar config_class:                 Class to be used when initiating the service's configuration in a new region/VPC
    """
    targets = (
        ('clusters', 'Clusters', 'list_clusters', {}, False),
    )
    region_config_class = EMRRegionConfig



########################################
# EMRVPCConfig
########################################

class EMRVPCConfig(object):
    """
    EMR configuration for a single VPC

    :ivar clusters:                     Dictionary of clusters [id]
    """

    def __init__(self):
        self.clusters = {}
