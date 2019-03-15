from ScoutSuite.providers.gcp.resources.resources import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.cloudsql.backups import Backups
from ScoutSuite.providers.gcp.resources.cloudsql.users import Users
from ScoutSuite.providers.utils import get_non_provider_id

class DatabaseInstances(GCPCompositeResources):
    _children = [ 
        (Backups, 'backups'),
        (Users, 'users')
    ]

    def __init__(self, gcp_facade, project_id):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_instances = await self.gcp_facade.cloudsql.get_database_instances(self.project_id)
        for raw_instance in raw_instances:
            instance_id, instance = self._parse_instance(raw_instance)
            self[instance_id] = instance
            await self._fetch_children(self[instance_id], gcp_facade = self.gcp_facade, project_id = self.project_id, instance_name = instance['name'])
            self[instance_id]['last_backup_timestamp'] = self._get_last_backup_timestamp(self[instance_id]['backups'])

    def _parse_instance(self, raw_instance):
        instance_dict = {}
        instance_dict['id'] = get_non_provider_id(raw_instance['name'])
        instance_dict['name'] = raw_instance['name']
        instance_dict['project_id'] = raw_instance['project']
        instance_dict['automatic_backup_enabled'] = raw_instance['settings']['backupConfiguration']['enabled']
        instance_dict['database_version'] = raw_instance['databaseVersion']
        instance_dict['log_enabled'] = self._is_log_enabled(raw_instance)
        instance_dict['ssl_required'] = self._is_ssl_required(raw_instance)
        instance_dict['authorized_networks'] = raw_instance['settings']['ipConfiguration']['authorizedNetworks']
        return instance_dict['id'], instance_dict

    def _is_log_enabled(self, raw_instance) :
        return raw_instance['settings']['backupConfiguration'].get('binaryLogEnabled')

    def _is_ssl_required(self, raw_instance):
        return raw_instance['settings']['ipConfiguration'].get('requireSsl')

    def _get_last_backup_timestamp(self, backups):
        if not backups:
            return 'N/A'

        last_backup_id = max(backups.keys(), key=(lambda k: backups[k]['creation_timestamp']))
        return backups[last_backup_id]['creation_timestamp']
        