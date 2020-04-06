from ScoutSuite.providers.aws.resources.base import AWSResources

from ScoutSuite.providers.utils import get_non_provider_id


class Buckets(AWSResources):
    async def fetch_all(self):
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
        raw_bucket['CreationDate'] = str(raw_bucket['CreationDate'])

        # If requested, get key properties
        raw_bucket['id'] = get_non_provider_id(raw_bucket['name'])
        return raw_bucket['id'], raw_bucket
