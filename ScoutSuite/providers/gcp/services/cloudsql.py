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

        super(CloudSQLConfig, self).__init__(thread_config)

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
        instance_dict['automatic_backup_status'] = 'Enabled' if instance['settings']['backupConfiguration'][
            'enabled'] else 'Disabled'
        instance_dict['log_status'] = 'Enabled' \
            if 'binaryLogEnagled' in instance['settings']['backupConfiguration'] \
               and instance['settings']['backupConfiguration']['binaryLogEnabled'] \
            else 'Disabled'
        instance_dict['ssl_required'] = 'Enabled' if ('requireSsl' in \
                                                      instance['settings']['ipConfiguration'] and \
                                                      instance['settings']['ipConfiguration']['requireSsl']) else 'Disabled'

        instance_dict['backups'] = self._get_instance_backups(instance, params)

        instance_dict['last_backup_timestamp'] = \
            instance_dict['backups'][max(instance_dict['backups'].keys(),
                                         key=(lambda k: instance_dict['backups'][k]['creation_timestamp']))]['creation_timestamp'] if \
                instance_dict['backups'].keys() else 'N/A'

        self.instances[instance_dict['id']] = instance_dict


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
