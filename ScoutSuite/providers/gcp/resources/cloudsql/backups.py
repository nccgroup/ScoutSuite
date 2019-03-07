# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Backups(Resources):
    def __init__(self, cloudsql_facade, project_id, instance_name):
        self.cloudsql_facade = cloudsql_facade
        self.project_id = project_id
        self.instance_name = instance_name

    async def fetch_all(self):
        raw_backups = await self.cloudsql_facade.get_backups(self.project_id, self.instance_name)
        for raw_backup in raw_backups:
            if raw_backup['status'] == 'SUCCESSFUL':
                backup_id, backup = self._parse_backup(raw_backup)
                self[backup_id] = backup

    def _parse_backup(self, raw_backup):
        backup_dict = {}
        backup_dict['id'] = raw_backup['id']
        backup_dict['backup_url'] = raw_backup['selfLink'],
        backup_dict['creation_timestamp'] = raw_backup['endTime'],
        backup_dict['status'] = raw_backup['status'],
        backup_dict['type'] = raw_backup['type']
        return backup_dict['id'], backup_dict
