from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .aliases import Aliases
from .keys import Keys


class KMS(Regions):
    _children = [
        (Aliases, 'aliases'),
        (Keys, 'keys'),
    ]

    def __init__(self, facade: AWSFacade):
        super(KMS, self).__init__('kms', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        await super(KMS, self).fetch_all(regions, excluded_regions, partition_name)
