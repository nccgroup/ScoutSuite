from ScoutSuite.providers.aws.resources.base import AWSResources


class PeeringConnections(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_peering_connections = await self.facade.ec2.get_peering_connections(self.scope['region'])
        for raw_peering_connection in raw_peering_connections:
            id, peering_connection = self._parse_peering_connections(raw_peering_connection)
            self[id] = peering_connection

    def _parse_peering_connections(self, raw_peering_connection):
        return raw_peering_connection[raw_peering_connection['VpcPeeringConnectionId']], raw_peering_connection
