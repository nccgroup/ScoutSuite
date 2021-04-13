from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class PeeringConnections(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.facade = facade
        self.region = region
        self.partition = facade.partition
        self.service = 'vpc'
        self.resource_type = 'peering-connection'

    async def fetch_all(self):
        raw_peering_connections = await self.facade.ec2.get_peering_connections(self.region)

        for raw_peering_connection in raw_peering_connections:
            id, peering_connection = self._parse_peering_connections(raw_peering_connection)
            self[id] = peering_connection

    def _parse_peering_connections(self, raw_peering_connection):
        raw_peering_connection['id'] = raw_peering_connection['name'] = raw_peering_connection['VpcPeeringConnectionId']
        raw_peering_connection['arn'] = format_arn(self.partition, self.service, self.region, '', raw_peering_connection['VpcPeeringConnectionId'], self.resource_type)
        return raw_peering_connection['id'], raw_peering_connection
