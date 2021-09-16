from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class Connections(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'directconnect'
        self.resource_type = 'connection'

    async def fetch_all(self):
        raw_connections = await self.facade.directconnect.get_connections(self.region)
        for raw_connection in raw_connections:
            name, resource = self._parse_connection(raw_connection)
            self[name] = resource

    def _parse_connection(self, raw_connection):
        raw_connection['id'] = raw_connection.pop('connectionId')
        raw_connection['name'] = raw_connection.pop('connectionName')
        raw_connection['arn'] = format_arn(self.partition, self.service, self.region, raw_connection.get('ownerAccount'), raw_connection.get('id'), self.resource_type)
        return raw_connection['id'], raw_connection
