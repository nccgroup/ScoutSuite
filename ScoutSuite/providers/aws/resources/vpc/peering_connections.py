from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class PeeringConnections(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.facade = facade
        self.region = region

    async def fetch_all(self):
        raw_peering_connections = await self.facade.ec2.get_peering_connections(self.region)

        for raw_peering_connection in raw_peering_connections:
            id, peering_connection = self._parse_peering_connections(raw_peering_connection)
            self[id] = peering_connection

    def _parse_peering_connections(self, raw_peering_connection):
        raw_peering_connection['id'] = get_non_provider_id(raw_peering_connection['VpcPeeringConnectionId'])
        raw_peering_connection['name'] = raw_peering_connection['VpcPeeringConnectionId']
        return raw_peering_connection['id'], raw_peering_connection
