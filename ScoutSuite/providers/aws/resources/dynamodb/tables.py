from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Tables(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Tables, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_tables = await self.facade.dynamodb.get_tables(self.region)
        for raw_table in raw_tables:
            name, resource = self._parse_table(raw_table)
            self[name] = resource

    def _parse_table(self, raw_table):
        table_dict = {}
        table_dict['name'] = raw_table.get('TableName')
        table_dict['id'] = raw_table.get('TableId')
        table_dict['arn'] = raw_table.get('TableArn')
        table_dict['attribute_definitions'] = raw_table.get('AttributeDefinitions')
        table_dict['key_schema'] = raw_table.get('KeySchema')
        table_dict['table_status'] = raw_table.get('TableStatus')
        table_dict['creation_date_time'] = raw_table.get('CreationDateTime')
        table_dict['provisioned_throughput'] = raw_table.get('ProvisionedThroughput')
        table_dict['table_size_bytes'] = raw_table.get('TableSizeBytes')
        table_dict['item_count'] = raw_table.get('ItemCount')
        table_dict['backup_summaries'] = raw_table.get('BackupSummaries')
        table_dict['continuous_backups'] = raw_table.get('ContinuousBackups')
        table_dict['tags'] = raw_table.get('tags')

        table_dict['automatic_backups_enabled'] = \
            raw_table['ContinuousBackups']['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus'] == 'ENABLED' \
                if 'ContinuousBackups' in raw_table else None

        if "SSEDescription" in raw_table:
            table_dict["sse_enabled"] = True
        else:
            table_dict["sse_enabled"] = False

        return table_dict['id'], table_dict
