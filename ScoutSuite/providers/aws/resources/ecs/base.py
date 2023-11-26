from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.ecs.clusters import Clusters
from ScoutSuite.providers.aws.resources.ecs.services import Services
from ScoutSuite.providers.aws.resources.ecs.tasks import Tasks
from ScoutSuite.providers.aws.resources.regions import Regions


class ECS(Regions):
    _children = [
        (Clusters, 'clusters'),
        (Services, 'services'),
        (Tasks,'tasks')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('ecs', facade)
