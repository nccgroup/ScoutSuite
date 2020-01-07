from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.cloudsql.backups import Backups
from ScoutSuite.providers.gcp.resources.cloudsql.users import Users
from ScoutSuite.providers.utils import get_non_provider_id


class DatabaseInstances(GCPCompositeResources):
    _children = [
        (Backups, 'backups'),
        (Users, 'users')
    ]

    def __init__(self, facade: GCPFacade, project_id: str):
        super(DatabaseInstances, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_instances = await self.facade.cloudsql.get_database_instances(self.project_id)
        for raw_instance in raw_instances:
            instance_id, instance = self._parse_instance(raw_instance)
            self[instance_id] = instance
        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={instance_id: {'project_id': self.project_id, 'instance_name': instance['name']}
                    for instance_id, instance in self.items()})
        self._set_last_backup_timestamps(self.items())

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

        # check if is or has a failover replica
        instance_dict['has_failover_replica'] = raw_instance.get('failoverReplica', []) != []
        instance_dict['is_failover_replica'] = raw_instance.get('masterInstanceName', '') != ''

        # network interfaces
        instance_dict['public_ip'] = None
        instance_dict['private_ip'] = None
        for address in raw_instance.get('ipAddresses', []):
            if address['type'] == 'PRIMARY':
                instance_dict['public_ip'] = address['ipAddress']
            elif address['type'] == 'PRIVATE':
                instance_dict['private_ip'] = address['ipAddress']
            else:
                print_exception('Unknown Cloud SQL instance IP address type: {}'.format(address['type']))

        return instance_dict['id'], instance_dict

    def _is_log_enabled(self, raw_instance):
        return raw_instance['settings']['backupConfiguration'].get('binaryLogEnabled')

    def _is_ssl_required(self, raw_instance):
        return raw_instance['settings']['ipConfiguration'].get('requireSsl', False)

    def _set_last_backup_timestamps(self, instances):
        for instance_id, _ in instances:
            self[instance_id]['last_backup_timestamp'] = self._get_last_backup_timestamp(
                self[instance_id]['backups'])

    def _get_last_backup_timestamp(self, backups):
        if not backups:
            return None
        last_backup_id = max(backups.keys(), key=(
            lambda k: backups[k]['creation_timestamp']))
        return backups[last_backup_id]['creation_timestamp']
