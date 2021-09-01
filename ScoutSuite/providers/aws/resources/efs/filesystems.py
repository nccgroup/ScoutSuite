from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn


class FileSystems(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'elasticfilesystem'
        self.resource_type = 'file-system'

    async def fetch_all(self):
        raw_file_systems = await self.facade.efs.get_file_systems(self.region)
        for raw_file_system in raw_file_systems:
            name, resource = self._parse_file_system(raw_file_system)
            self[name] = resource

    def _parse_file_system(self, raw_file_system):
        fs_id = raw_file_system.pop('FileSystemId')
        raw_file_system['name'] = raw_file_system.pop('Name') if 'Name' in raw_file_system else None
        raw_file_system['tags'] = raw_file_system.pop('Tags')
        raw_file_system['arn'] = format_arn(self.partition, self.service, self.region, raw_file_system.get('OwnerId'), fs_id, self.resource_type)
        return fs_id, raw_file_system
