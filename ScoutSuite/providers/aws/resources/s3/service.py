from ScoutSuite.providers.aws.facade.facade import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources, AWSCompositeResources

from ScoutSuite.providers.utils import get_non_provider_id


class Bucket(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_buckets = await self.facade.s3.get_buckets()
        for raw_bucket in raw_buckets:
            name, resource = self._parse_bucket(raw_bucket)
            self[name] = resource

    def _parse_bucket(self, raw_bucket):
        """
        Parse a single S3 bucket

        TODO:
        - CORS
        - Lifecycle
        - Notification ?
        - Get bucket's policy

        :param bucket:
        :param params:
        :return:
        """
        raw_bucket['name'] = raw_bucket.pop('Name')
        # api_client = params['api_clients'][get_s3_list_region(list(params['api_clients'].keys())[0])]

        raw_bucket['CreationDate'] = str(raw_bucket['CreationDate'])

        # get_s3_bucket_policy(api_client, bucket['name'], bucket)
        # get_s3_bucket_secure_transport(api_client, bucket['name'], bucket)
        # # If requested, get key properties
        raw_bucket['id'] = get_non_provider_id(raw_bucket['name'])
        return raw_bucket['id'], raw_bucket



class S3(AWSCompositeResources):
    _children = [
        (Bucket, 'buckets')
    ]

    def __init__(self):
        super(S3, self).__init__('s3', {})
        # TODO: Should be injected
        self.facade = AWSFacade()

    async def fetch_all(self, credentials, regions=None, partition_name='aws'):
        # TODO: This should not be set here, the facade should be injected and already authenticated
        self.facade._set_session(credentials)
        await self._fetch_children(self, {})
