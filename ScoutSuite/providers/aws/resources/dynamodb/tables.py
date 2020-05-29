from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Tables(AWSResources):
    def __init__(self, facade: AWSFacade, region: str) -> None:
        super(Tables, self).__init__(facade)
        self.region = region

    async def fetch_all(self, **kwargs):
        raw_tables = await self.facade.dynamodb.get_tables(self.region)
        for raw_table in raw_tables:
            name, resource = await self._parse_table(raw_table)

    async def _parse_table(self, raw_table):
        table = {}
        table['name'] = raw_table
