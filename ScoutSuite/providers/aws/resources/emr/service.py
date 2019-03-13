from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.vpcs import Vpcs
from ScoutSuite.providers.aws.resources.resources import AWSResources


class EMRClusters(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_clusters = await self.facade.emr.get_clusters(self.scope['region'])
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
        raw_cluster['id'] = raw_cluster.pop('Id')
        raw_cluster['name'] = raw_cluster.pop('Name')
        vpc_id = 'TODO'  # The EMR API won't disclose the VPC ID, so wait until all configs have been fetch and look
        # # up the VPC based on the subnet ID
        # manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
        return raw_cluster['id'], raw_cluster


class EMRVpcs(Vpcs):
    children: [
        (EMRClusters, 'clusters')
    ]


class EMR(Regions):
    _children = [
        (EMRVpcs, 'vpcs')
    ]

    def __init__(self):
        super(EMR, self).__init__('emr')


# # -*- coding: utf-8 -*-

# from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
# from ScoutSuite.providers.aws.configs.vpc import VPCConfig
# from ScoutSuite.utils import manage_dictionary


# ########################################
# # EMRRegionConfig
# ########################################

# class EMRRegionConfig(RegionConfig):
#     """
#     EMR configuration for a single AWS region
#     """

#     def parse_cluster(self, global_params, region, cluster):
#         """
#         Parse a single EMR cluster

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param cluster:                 EMR cluster
#         """
#         cluster_id = cluster['Id']
#         cluster = api_clients[region].describe_cluster(ClusterId=cluster_id)['Cluster']
#         cluster['id'] = cluster.pop('Id')
#         cluster['name'] = cluster.pop('Name')
#         vpc_id = 'TODO'  # The EMR API won't disclose the VPC ID, so wait until all configs have been fetch and look
#         # up the VPC based on the subnet ID
#         manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
#         self.vpcs[vpc_id].clusters[cluster_id] = cluster


# ########################################
# # EMRConfig
# ########################################

# class EMRConfig(RegionalServiceConfig):
#     """
#     EMR configuration for all AWS regions
#     """

#     region_config_class = EMRRegionConfig

#     def __init__(self, service_metadata, thread_config=4):
#         super(EMRConfig, self).__init__(service_metadata, thread_config)
