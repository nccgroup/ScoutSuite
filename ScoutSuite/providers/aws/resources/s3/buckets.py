from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import format_arn, get_partition_name
from ScoutSuite.providers.utils import get_non_provider_id


class Buckets(AWSResources):
    async def fetch_all(self):
        self.partition = get_partition_name(self.facade.session)
        self.service = 's3'
        
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

        raw_bucket['id'] = get_non_provider_id(raw_bucket['name'])
        # Passing empty strings for 'region' and 'account-id' since S3 bucket ARNs omit them
        raw_bucket['arn'] = format_arn(self.partition, self.service, '', '', '*', raw_bucket['name'])
        return raw_bucket['id'], raw_bucket
