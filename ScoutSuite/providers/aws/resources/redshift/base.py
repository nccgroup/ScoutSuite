from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .cluster_parameter_groups import ClusterParameterGroups
from .cluster_security_groups import ClusterSecurityGroups
from .vpcs import RedshiftVpcs


class Redshift(Regions):
    _children = [
        (RedshiftVpcs, 'vpcs'),
        (ClusterParameterGroups, 'parameter_groups'),
        (ClusterSecurityGroups, 'security_groups')
    ]

    def __init__(self, facade: AWSFacade):
        super(Redshift, self).__init__('redshift', facade)
