from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .backups import Backups


class DynamoDB(Regions):
    _children = [(Backups, "backups")]

    def __init__(self, facade: AWSFacade):
        super(Backups, self).__init__("backups", facade)
