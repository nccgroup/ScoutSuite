from ScoutSuite.providers.aws.resources.vpcs import Vpcs
from ScoutSuite.providers.aws.resources.elasticache.cluster import Clusters
from ScoutSuite.providers.aws.resources.elasticache.subnetgroups import SubnetGroups


class ElastiCacheVpcs(Vpcs):
    _children = [
        (Clusters, 'clusters'),
        (SubnetGroups, 'subnet_groups')
    ]

    def __init__(self, facade, scope: dict):
        super(ElastiCacheVpcs, self).__init__(facade, scope, add_ec2_classic=True)
