# -*- coding: utf-8 -*-

from opinel.utils.console import printError

from ScoutSuite.providers.gcp.configs.base import GCPBaseConfig


class CloudStorageConfig(GCPBaseConfig):
    targets = (
        ('buckets', 'Buckets', 'list_buckets', {'project': '{{project_placeholder}}'}, False),
    )

    def __init__(self, thread_config):
        self.library_type = 'cloud_client_library'

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
        bucket_dict['id'] = self.get_non_provider_id(bucket.id)
        bucket_dict['name'] = bucket.name

        for project in self.projects:
            if str(project['projectNumber']) == str(bucket.project_number):
                bucket_dict['project_id'] = project['projectId']
                break

        bucket_dict['project_number'] = bucket.project_number
        bucket_dict['creation_date'] = bucket.time_created
        bucket_dict['location'] = bucket.location
        bucket_dict['storage_class'] = bucket.storage_class.lower()
        bucket_dict['versioning_status_enabled'] = bucket.versioning_enabled

        get_cloudstorage_bucket_logging(bucket, bucket_dict)
        get_cloudstorage_bucket_acl(bucket, bucket_dict)

        self.buckets[bucket_dict['id']] = bucket_dict


def get_cloudstorage_bucket_logging(bucket, bucket_dict):
    try:
        bucket_dict['logging_enabled'] = bucket.get_logging() is not None
        return True
    except Exception as e:
        printError('Failed to get bucket logging configuration for %s: %s' % (bucket.name, e))
        bucket_dict['logging_enabled'] = None
        return False


def get_cloudstorage_bucket_acl(bucket, bucket_dict):
    try:

        bucket_acls = bucket.get_iam_policy()

        bucket_dict['acl_configuration'] = {}
        for role in bucket_acls._bindings:
            for member in bucket_acls[role]:
                if member.split(':')[0] not in ['projectEditor', 'projectViewer', 'projectOwner']:
                    if member not in bucket_dict['acl_configuration']:
                        bucket_dict['acl_configuration'][member] = [role]
                    else:
                        bucket_dict['acl_configuration'][member].append(role)

        return True
    except Exception as e:
        printError('Failed to get bucket ACL configuration for %s: %s' % (bucket.name, e))
        bucket_dict['acls'] = 'Unknown'
        return False
