from ScoutSuite.core.console import print_exception, print_warning
from ScoutSuite.providers.aws.facade.base import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently, map_concurrently


class DynamoDBFacade(AWSBaseFacade):
    _GET_TABLES_BATCH_SIZE = 100

    async def get_tables(self, region):
        try:
            tables_names = await AWSFacadeUtils.get_all_pages('dynamodb', region, self.session, 'list_tables',
                                                              'TableNames')
            return await map_concurrently(self._get_table, tables_names, region=region)
        except Exception as e:
            print_exception('Failed to get DynamoDB tables: {}'.format(e))
            return []

    async def _get_table(self, table_name: str, region: str):
        client = AWSFacadeUtils.get_client('dynamodb', self.session, region)

        try:
            table = await run_concurrently(lambda: client.describe_table(TableName=table_name)['Table'])
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                print_warning('Failed to get DynamoDB table: {}'.format(e))
            else:
                print_exception('Failed to get DynamoDB table: {}'.format(e))
        else:
            await get_and_set_concurrently(
                [self._get_and_set_backup, self._get_and_set_continuous_backups, self._get_and_set_tags],
                [table],
                region=region)

        return table

    async def _get_and_set_backup(self, table: {}, region: str):
        client = AWSFacadeUtils.get_client('dynamodb', self.session, region)

        try:
            summaries = await run_concurrently(lambda: client.list_backups(TableName=table['TableName']))
            table['BackupSummaries'] = summaries.get('BackupSummaries')
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                print_warning('Failed to list DynamoDB table backups: {}'.format(e))
            else:
                print_exception('Failed to list DynamoDB table backups: {}'.format(e))

    async def _get_and_set_continuous_backups(self, table: {}, region: str):
        client = AWSFacadeUtils.get_client('dynamodb', self.session, region)

        try:
            description = await run_concurrently(
                lambda: client.describe_continuous_backups(TableName=table['TableName']))
            table['ContinuousBackups'] = description.get('ContinuousBackupsDescription')
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                print_warning('Failed to describe DynamoDB table continuous backups: {}'.format(e))
            else:
                print_exception('Failed to describe DynamoDB table continuous backups: {}'.format(e))

    async def _get_and_set_tags(self, table: {}, region: str):
        client = AWSFacadeUtils.get_client('dynamodb', self.session, region)

        try:
            tags = await run_concurrently(
                lambda: client.list_tags_of_resource(ResourceArn=table['TableArn']))
            table['tags'] = tags.get('Tags')
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                print_warning('Failed to describe DynamoDB table tags: {}'.format(e))
            else:
                print_exception('Failed to describe DynamoDB table tags: {}'.format(e))

