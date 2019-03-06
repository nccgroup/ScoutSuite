from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class FileSystems(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_file_systems  = self.facade.efs.get_file_systems(self.scope['region'])
        for raw_file_system in raw_file_systems:
            name, resource = self._parse(raw_file_system)
            self[name] = resource

    def _parse(self, raw_file_system):
        fs_id = raw_file_system.pop('FileSystemId')
        raw_file_system['name'] = raw_file_system.pop('Name') if 'Name' in raw_file_system else None

        # Get tags
        raw_file_system['tags'] = raw_file_system.pop('Tags')
        
        return fs_id, raw_file_system



class EFS(Regions):
    _children = [
        (FileSystems, 'filesystems')
    ]

    def __init__(self):
        super(EFS, self).__init__('efs')
