from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Tables(AWSResources):
    def __init__(self, facade: AWSFacade, region: str) -> None:
        super(Tables, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_tables = await self.facade.dynamodb.get_tables(self.region)
        for raw_table in raw_tables:
            name, resource = await self._parse_table(raw_table)
            self[name] = resource

    async def _parse_table(self, raw_table):
        table = {}
        t, resource = await self.facade.dynamodb.get_table(self.region, raw_table)
        table = {**table, **resource}
        return raw_table, table
