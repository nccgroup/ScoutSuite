from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.eks.clusters import Clusters
from ScoutSuite.providers.aws.resources.eks.nodegroups import Nodegroups
from ScoutSuite.providers.aws.resources.regions import Regions

class EKS(Regions):
    _children = [
        (Clusters, 'clusters'),
        (Nodegroups,'nodegroups')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('eks', facade)

