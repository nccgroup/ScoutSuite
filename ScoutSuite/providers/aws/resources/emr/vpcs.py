from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources

from .clusters import EMRClusters


class EMRVpcs(AWSCompositeResources):
    _children = [
        (EMRClusters, 'clusters')
    ]

    def __init__(self, facade: AWSFacade, region: str):
        self.region = region

        super().__init__(facade)

    async def fetch_all(self):
        # EMR won't disclose its VPC, so we put everything in a VPC named "EMR-UNKNOWN-VPC", and we
        # infer the VPC afterwards during the preprocessing.
        tmp_vpc = 'EMR-UNKNOWN-VPC'
        self[tmp_vpc] = {}
        await self._fetch_children(self[tmp_vpc], {'region': self.region})
