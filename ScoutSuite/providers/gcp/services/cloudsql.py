# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig

from opinel.utils.console import printError, printException, printInfo


class CloudSQLConfig(GCPBaseConfig):
    targets = (
        ('databases', 'Databases', 'list_buckets', {}, False),
    )

    def __init__(self, thread_config):

        self.library_type = 'api_client_library'

        self.databases = {}
        self.database_count = 0
        super(CloudSQLConfig, self).__init__(thread_config)

    def parse_databases(self, database, params):
        """
        Parse a single Cloud Storage bucket

        :param bucket: Bucket object  representing a single bucket
        :param params: Dictionary of parameters, including API client
        :return: None
        """
        api_client = params['api_client']

        database._client = api_client

        database_dict = {}
        database_dict['id'] = database.id

        self.databases[database_dict['id']] = database_dict
