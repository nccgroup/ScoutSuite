from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class FileSystems(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_file_systems = await self.facade.efs.get_file_systems(self.region)
        parsing_error_counter = 0
        for raw_file_system in raw_file_systems:
            try:
                name, resource = self._parse_file_system(raw_file_system)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_file_system(self, raw_file_system):
        fs_id = raw_file_system.pop('FileSystemId')
        raw_file_system['name'] = raw_file_system.pop('Name') if 'Name' in raw_file_system else None
        raw_file_system['tags'] = raw_file_system.pop('Tags')

        return fs_id, raw_file_system
