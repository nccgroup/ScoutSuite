from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class RouteTables(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.facade = facade
        self.region = region

    async def fetch_all(self):
        raw_route_tables = await self.facade.ec2.get_route_tables(self.region)
        for raw_route_table in raw_route_tables:
            id, route_table = self._parse_route_tables(raw_route_table)
            self[id] = route_table

    def _parse_route_tables(self, raw_route_table):
        pass
        # return route_table_id, raw_route_tables
