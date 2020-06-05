
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Backups(AWSResources):

    def __init__(self, facade: AWSFacade, region: str) -> None:
        super(Backups, self).__init__(facade)
        self.region = region


    async def fetch_all(self):
        raw_backups = await self.facade.dynamodb.get_backups(self.region)
        for raw_backup in raw_backups:
            name, resource = await self._parse_backup(raw_backup)
            self[name] = resource


    async def _parse_backup(self, raw_backup):
        backup = {
            'table_name': raw_backup.get('TableName'),
            'id': raw_backup.get('TableId'),
            'arn': raw_backup.get('TableArn'),
        }
        return backup['table_name'], backup
