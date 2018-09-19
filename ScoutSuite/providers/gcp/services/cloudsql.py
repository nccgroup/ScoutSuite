# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo


class CloudSQLConfig(GCPBaseConfig):
    targets = (
        ('instances', 'Instances', 'list', {'project': 'project_placeholder'}, False),
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

        instance_dict['automatic_backup_status'] = 'Enabled' if instance['settings']['backupConfiguration']['enabled'] else 'Disabled'
        instance_dict['log_status'] = 'Enabled' if instance['settings']['backupConfiguration']['binaryLogEnabled'] else 'Disabled'
        # TODO test this
        instance_dict['ssl_required'] = 'Enabled' if ('requireSsl' in \
                                                     instance['settings']['ipConfiguration'] and \
                                                     instance['settings']['ipConfiguration']['requireSsl']) else 'Disabled'

        instance_dict['backups'] = self._get_instance_backups(instance, params)

        self.instances[instance_dict['id']] = instance_dict


    def _get_instance_backups(self, instance, params):
        backups = params['api_client'].backupRuns().list(project=instance['project'],
                                                         instance=instance['name']).execute()
        try:
            backups_dict = {}
            for backup in backups['items']:
                backups_dict[backup['id']] = {
                    'backup_url': backup['selfLink'],
                    'creation_timestamp': backup['endTime'],
                    'status': backup['status'],
                    'type': backup['type']
                }
            return backups_dict
        except Exception as e:
            printError('Failed to get backups for SQL instance %s: %s' % (instance['name'], e))
            return None
