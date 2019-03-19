from asyncio import Lock
from botocore.exceptions import ClientError

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_error, print_exception


class S3Facade(AWSBaseFacade):

    async def get_buckets(self):
        client = AWSFacadeUtils.get_client('s3', None, self.session)
        buckets = (await run_concurrently(lambda: client.list_buckets()))['Buckets']

        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket['region'] = await self._get_s3_bucket_location(bucket_name)
            await self._set_s3_bucket_logging(bucket)
            await self._set_s3_bucket_versioning(bucket)
            await self._set_s3_bucket_webhosting(bucket)
            await self._set_s3_bucket_default_encryption(bucket)

        return buckets

    async def _get_s3_bucket_location(self, bucket_name):
        client = AWSFacadeUtils.get_client('s3', None, self.session)
        location = client.get_bucket_location(Bucket=bucket_name)
        region = location['LocationConstraint'] if location['LocationConstraint'] else 'us-east-1'

        # Fixes issue #59: location constraint can be either EU or eu-west-1 for Ireland...
        if region == 'EU':
            region = 'eu-west-1'

        return region

    async def _set_s3_bucket_logging(self, bucket):
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            logging = await run_concurrently(lambda: client.get_bucket_logging(Bucket=bucket['Name']))
        except Exception as e:
            print_error('Failed to get logging configuration for %s: %s' % (bucket['Name'], e))
            bucket['logging'] = 'Unknown'

        if 'LoggingEnabled' in logging:
            bucket['logging'] = logging['LoggingEnabled']['TargetBucket'] + '/' + logging['LoggingEnabled']['TargetPrefix']
        else:
            bucket['logging'] = 'Disabled'

    # noinspection PyBroadException
    async def _set_s3_bucket_versioning(self, bucket):
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            versioning = await run_concurrently(lambda: client.get_bucket_versioning(Bucket=bucket['Name']))
            bucket['versioning_status_enabled'] = self._status_to_bool(versioning.get('Status'))
            bucket['version_mfa_delete_enabled'] = self._status_to_bool(versioning.get('MFADelete'))
        except Exception:
            bucket['versioning_status_enabled'] = None
            bucket['version_mfa_delete_enabled'] = None


    # noinspection PyBroadException
    async def _set_s3_bucket_webhosting(self, bucket):
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            result = client.get_bucket_website(Bucket=bucket['Name'])
            bucket['web_hosting_enabled'] = 'IndexDocument' in result
        except Exception:
            # TODO: distinguish permission denied from  'NoSuchWebsiteConfiguration' errors
            bucket['web_hosting_enabled'] = False

    async def _set_s3_bucket_default_encryption(self, bucket):
        bucket_name = bucket['Name']
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            await run_concurrently(lambda: client.get_bucket_encryption(Bucket=bucket['Name']))
            bucket['default_encryption_enabled'] = True
        except ClientError as e:
            if 'ServerSideEncryptionConfigurationNotFoundError' in e.response['Error']['Code']:
                bucket['default_encryption_enabled'] = False
            else:
                print_error('Failed to get encryption configuration for %s: %s' % (bucket_name, e))
                bucket['default_encryption_enabled'] = None
        except Exception as e:
            print_error('Failed to get encryption configuration for %s: %s' % (bucket_name, e))
            bucket['default_encryption'] = 'Unknown'
            
    @staticmethod
    def _status_to_bool(value):
        """ Converts a string to True if it is equal to 'Enabled' or to False otherwise. """
        return value == 'Enabled'

