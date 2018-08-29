# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.configs.base import BaseConfig

class CloudStorageConfig(BaseConfig):

    targets = (
        ('buckets', 'Buckets', 'list', {'project': 'ncccon2018prjct'}, False),  # TODO this is hardcoded
    )

    def __init__(self, thread_config):
        self.buckets = {}
        self.buckets_count = 0
        super(CloudStorageConfig, self).__init__(thread_config)

    def parse_buckets(self, bucket, params):
        """
        Parse a single S3 bucket

        :param bucket:
        :param params:
        :return:
        """
        # bucket['name'] = bucket.pop('Name')
        # bucket['CreationDate'] = str(bucket['CreationDate'])
        # bucket['id'] = self.get_non_aws_id(bucket['name'])
        # self.buckets[bucket['id']] = bucket

        bucket['id'] = bucket['id']
        bucket['name'] = bucket['name']
        bucket['CreationDate'] = bucket['timeCreated']
        self.buckets[bucket['id']] = bucket
