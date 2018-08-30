# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import BaseConfig

from opinel.utils.console import printError, printException, printInfo


class CloudStorageConfig(BaseConfig):
    targets = (
        ('buckets', 'Buckets', 'list_buckets', {}, False),
    )

    def __init__(self, thread_config):
        self.buckets = {}
        self.buckets_count = 0
        super(CloudStorageConfig, self).__init__(thread_config)

    def parse_buckets(self, bucket, params):
        """
        Parse a single Cloud Storage bucket

        :param bucket: Bucket object  representing a single bucket
        :param params: Dictionary of parameters, including API client
        :return: None
        """
        api_client = params['api_client']

        bucket._client = api_client

        bucket_dict = {}
        bucket_dict['id'] = bucket.id
        bucket_dict['name'] = bucket.name
        bucket_dict['creation_date'] = bucket.time_created
        bucket_dict['location'] = bucket.location.lower()
        bucket_dict['storage_class'] = bucket.storage_class.lower()

        bucket_dict['versioning_status'] = 'Enabled' if bucket.versioning_enabled else 'Disabled'

        get_cloudstorage_bucket_logging(api_client, bucket, bucket_dict)

        self.buckets[bucket_dict['id']] = bucket_dict

def get_cloudstorage_bucket_logging(api_client, bucket, bucket_dict):

    try:
        logging = bucket.get_logging()
        if logging:
            bucket_dict['logging_status'] = 'Enabled'
        else:
            bucket_dict['logging_status'] = 'Disabled'
        return True
    except Exception as e:
        printError('Failed to get logging configuration for %s: %s' % (bucket.name, e))
        bucket_dict['logging_status'] = 'Unknown'
        return False
