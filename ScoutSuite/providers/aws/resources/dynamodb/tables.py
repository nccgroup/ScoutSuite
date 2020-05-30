from debugpy.common.log import debug
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Tables(AWSResources):
    def __init__(self, facade: AWSFacade, region: str) -> None:
        super(Tables, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        tables = await self.facade.dynamodb.get_tables(self.region)
        for table_name in tables:
            raw_table = await self.facade.dynamodb.get_table(self.region, table_name)
            table = await self._parse_table(raw_table)
            self[table_name] = table

    async def _parse_table(self, raw_table):
        table = {}
        if raw_table["Table"]:
            raw = raw_table["Table"]
            if "SSEDescription" in raw:
                table["sse_description"] = raw["SSEDescription"]
                table["sse_enabled"] = True
            else:
                table["sse_enabled"] = False
            if "ArchivalSummary" in raw:
                table["archival_summary"] = raw["ArchivalSummary"]
        return table
