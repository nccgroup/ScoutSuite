# -*- coding: utf-8 -*-

from opinel.utils.console import printError

import operator
from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class CloudSQLConfig(GCPBaseConfig):
    targets = (
        ('instances', 'Instances', 'list', {'project': '{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):

        self.library_type = 'api_client_library'

        self.instances = {}
        self.instances_count = 0

        # TODO figure out why GCP returns errors when running with more then 1 thread (multithreading)
        super(CloudSQLConfig, self).__init__(thread_config=1)

    def parse_instances(self, instance, params):
        """
        Parse a single Cloud Storage bucket

        :param bucket: Bucket object  representing a single bucket
        :param params: Dictionary of parameters, including API client
        :return: None
        """
        instance_dict = {}
        instance_dict['id'] = self.get_non_provider_id(instance['name'])
        instance_dict['name'] = instance['name']
        instance_dict['project_id'] = instance['project']
        instance_dict['automatic_backup_enabled'] = instance['settings']['backupConfiguration']['enabled']
        instance_dict['database_version'] = instance['databaseVersion']
        instance_dict['log_enabled'] = self._is_log_enabled(instance)
        instance_dict['ssl_required'] = self._is_ssl_required(instance)
        instance_dict['backups'] = self._get_instance_backups(instance, params)
        instance_dict['users'] = self._get_users(instance, params)
        instance_dict['authorized_networks'] = instance['settings']['ipConfiguration']['authorizedNetworks']

        instance_dict['last_backup_timestamp'] = \
            instance_dict['backups'][max(instance_dict['backups'].keys(),
                                         key=(lambda k: instance_dict['backups'][k]['creation_timestamp']))]['creation_timestamp'] if \
                instance_dict['backups'].keys() else 'N/A'

        self.instances[instance_dict['id']] = instance_dict

    def _get_users(self, instance, params):
        users_dict = {}

        try:
            users = params['api_client'].users().list(project=instance['project'], instance=instance['name']).execute()
            for user in users['items']:
                users_dict[user['name']] = self._parse_user(user)

        except Exception as e:
            printError('Failed to fetch users for SQL instance %s: %s' % (instance['name'], e))
            
        return users_dict

    def _parse_user(self, user):
        user_dict = {}
        user_dict['name'] = user['name']
        user_dict['host'] = user.get('host')
        return user_dict

    def _get_instance_backups(self, instance, params):

        backups_dict = {}

        try:
            backups = params['api_client'].backupRuns().list(project=instance['project'],
                                                             instance=instance['name']).execute()
        # this is triggered when there are no backups
        except AttributeError as e:
            return backups_dict
        except Exception as e:
            printError('Failed to fetch backups for SQL instance %s: %s' % (instance['name'], e))
            return backups_dict

        try:
            if 'items' in backups:
                for backup in backups['items']:
                    if backup['status'] == 'SUCCESSFUL':
                        backups_dict[backup['id']] = {
                            'backup_url': backup['selfLink'],
                            'creation_timestamp': backup['endTime'],
                            'status': backup['status'],
                            'type': backup['type']
                        }

            return backups_dict

        except Exception as e:
            printError('Failed to parse backups for SQL instance %s: %s' % (instance['name'], e))
            return None

    def _is_log_enabled(self, instance) :
        return instance['settings']['backupConfiguration'].get('binaryLogEnabled')

    def _is_ssl_required(self, instance):
        return instance['settings']['ipConfiguration'].get('requireSsl')