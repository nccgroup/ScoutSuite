from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class PeeringConnections(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.facade = facade
        self.region = region

    async def fetch_all(self):
        raw_peering_connections = await self.facade.ec2.get_peering_connections(self.region)
        parsing_error_counter = 0

        for raw_peering_connection in raw_peering_connections:
            try:
                id, peering_connection = self._parse_peering_connections(raw_peering_connection)
                self[id] = peering_connection
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_peering_connections(self, raw_peering_connection):
        raw_peering_connection['id'] = raw_peering_connection['name'] = raw_peering_connection['VpcPeeringConnectionId']
        return raw_peering_connection['id'], raw_peering_connection
