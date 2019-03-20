from ScoutSuite.providers.aws.resources.regions import Regions

from .vpcs import RedshiftVpcs
from .cluster_parameter_groups import ClusterParameterGroups
from .cluster_security_groups import ClusterSecurityGroups


class Redshift(Regions):
    _children = [
        (RedshiftVpcs, 'vpcs'),
        (ClusterParameterGroups, 'parameter_groups'),
        (ClusterSecurityGroups, 'security_groups')
    ]

    def __init__(self):
        super(Redshift, self).__init__('redshift')
