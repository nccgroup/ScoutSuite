from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import no_camel


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
                table["sse_enabled"] = True
            else:
                table["sse_enabled"] = False
            new_dict = await self.camel_keys(raw)
            table.update(new_dict)

        return table

    async def camel_keys(self, d: dict) -> dict:
        new_table = {}
        for k in d.keys():
            new_key = no_camel(k)
            if type(d[k]) is dict:
                new_table[new_key] = await self.camel_keys(d[k])
            else:
                new_table[new_key] = d[k]
        return new_table
