from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Connections(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Connections, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_connections = await self.facade.directconnect.get_connections(self.region)
        for raw_connection in raw_connections:
            name, resource = self._parse_connection(raw_connection)
            self[name] = resource

    def _parse_connection(self, raw_connection):
        raw_connection['id'] = raw_connection.pop('connectionId')
        raw_connection['name'] = raw_connection.pop('connectionName')
        return raw_connection['id'], raw_connection
