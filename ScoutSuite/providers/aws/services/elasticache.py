# -*- coding: utf-8 -*-

from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from ScoutSuite.providers.aws.configs.vpc import VPCConfig
from ScoutSuite.utils import ec2_classic



########################################
# ElastiCacheRegionConfig
########################################

class ElastiCacheRegionConfig(RegionConfig):
    """
    ElastiCache configuration for a single AWS region
    """

    def parse_cluster(self, global_params, region, cluster):
        """
        Parse a single ElastiCache cluster

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 ElastiCache cluster
        """
        cluster_name = cluster.pop('CacheClusterId')
        cluster['name'] = cluster_name
        # Must fetch info about the subnet group to retrieve the VPC ID...
        if 'CacheSubnetGroupName' in cluster:
            subnet_group = api_clients[region].describe_cache_subnet_groups(CacheSubnetGroupName = cluster['CacheSubnetGroupName'])['CacheSubnetGroups'][0]
            vpc_id = subnet_group['VpcId']
        else:
            vpc_id = ec2_classic
            subnet_group = None
        manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
        self.vpcs[vpc_id].clusters[cluster_name] = cluster
        if subnet_group:
            self.vpcs[vpc_id].subnet_groups[subnet_group['CacheSubnetGroupName']] = subnet_group


    def parse_security_group(self, global_params, region, security_group):
        """
        Parse a single ElastiCache security group

        :param global_params:
        :param region:
        :param security_group:
        :return:
        """
        security_group['name'] = security_group.pop('CacheSecurityGroupName')
        self.security_groups[security_group['name']] = security_group



########################################
# ElastiCacheConfig
########################################

class ElastiCacheConfig(RegionalServiceConfig):
    """
    ElastiCache configuration for all AWS regions
    """

    region_config_class = ElastiCacheRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(ElastiCacheConfig, self).__init__(service_metadata, thread_config)
