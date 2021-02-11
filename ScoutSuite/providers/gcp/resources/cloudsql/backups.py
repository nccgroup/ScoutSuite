from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.core.console import print_exception


class Backups(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, instance_name: str):
        super().__init__(facade)
        self.project_id = project_id
        self.instance_name = instance_name

    async def fetch_all(self):
        raw_backups = await self.facade.cloudsql.get_backups(self.project_id, self.instance_name)
        parsing_error_counter = 0
        for raw_backup in raw_backups:
            try:
                if raw_backup['status'] == 'SUCCESSFUL':
                    backup_id, backup = self._parse_backup(raw_backup)
                    self[backup_id] = backup
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_backup(self, raw_backup):
        backup_dict = {}
        backup_dict['id'] = raw_backup['id']
        backup_dict['backup_url'] = raw_backup['selfLink'],
        backup_dict['creation_timestamp'] = raw_backup['endTime'],
        backup_dict['status'] = raw_backup['status'],
        backup_dict['type'] = raw_backup['type']
        return backup_dict['id'], backup_dict
