from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class FileSystems(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(FileSystems, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_file_systems = await self.facade.efs.get_file_systems(self.region)
        for raw_file_system in raw_file_systems:
            name, resource = self._parse_file_system(raw_file_system)
            self[name] = resource

    def _parse_file_system(self, raw_file_system):
        fs_id = raw_file_system.pop('FileSystemId')
        raw_file_system['name'] = raw_file_system.pop('Name') if 'Name' in raw_file_system else None
        raw_file_system['tags'] = raw_file_system.pop('Tags')

        return fs_id, raw_file_system
