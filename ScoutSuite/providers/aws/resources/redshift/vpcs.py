from ScoutSuite.providers.aws.resources.vpcs import Vpcs

from .clusters import Clusters


class RedshiftVpcs(Vpcs):
    _children = [
        (Clusters, 'clusters'),
    ]

    def __init__(self, facade, scope: dict):
        super(RedshiftVpcs, self).__init__(facade, scope, add_ec2_classic=True)
