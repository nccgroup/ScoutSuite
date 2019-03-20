from asyncio import Lock
import json
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
            await self._set_s3_acls(bucket)
            await self._set_s3_bucket_policy(bucket)

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
            
    async def _set_s3_acls(self, bucket, key_name=None):
        bucket_name = bucket['Name']
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            grantees = {}
            if key_name:
                grants = await run_concurrently(lambda: client.get_object_acl(Bucket=bucket_name, Key=key_name))
            else:
                grants =  await run_concurrently(lambda: client.get_bucket_acl(Bucket=bucket_name))
            for grant in grants['Grants']:
                if 'ID' in grant['Grantee']:
                    grantee = grant['Grantee']['ID']
                    display_name = grant['Grantee']['DisplayName'] if \
                        'DisplayName' in grant['Grantee'] else grant['Grantee']['ID']
                elif 'URI' in grant['Grantee']:
                    grantee = grant['Grantee']['URI'].split('/')[-1]
                    display_name = self._s3_group_to_string(grant['Grantee']['URI'])
                else:
                    grantee = display_name = 'Unknown'
                permission = grant['Permission']
                grantees.setdefault(grantee, {})
                grantees[grantee]['DisplayName'] = display_name
                if 'URI' in grant['Grantee']:
                    grantees[grantee]['URI'] = grant['Grantee']['URI']
                grantees[grantee].setdefault('permissions', self._init_s3_permissions())
                self._set_s3_permissions(grantees[grantee]['permissions'], permission)
            bucket['grantees'] = grantees
        except Exception as e:
            print_error('Failed to get ACL configuration for %s: %s' % (bucket_name, e))
            bucket['grantees'] = {}            

    async def _set_s3_bucket_policy(self, bucket):
        client = AWSFacadeUtils.get_client('s3', bucket['region'], self.session)
        try:
            bucket_policy =  await run_concurrently(lambda: client.get_bucket_policy(Bucket=bucket['Name']))
            bucket['policy'] = json.loads(bucket_policy['Policy'])
        except Exception as e:
            if not (type(e) == ClientError and e.response['Error']['Code'] == 'NoSuchBucketPolicy'):
                print_error('Failed to get bucket policy for %s: %s' % (bucket['Name'], e))

    @staticmethod
    def _init_s3_permissions():
        permissions = {'read': False, 'write': False, 'read_acp': False, 'write_acp': False}
        return permissions

    @staticmethod
    def _set_s3_permissions(permissions, name):
        if name == 'READ' or name == 'FULL_CONTROL':
            permissions['read'] = True
        if name == 'WRITE' or name == 'FULL_CONTROL':
            permissions['write'] = True
        if name == 'READ_ACP' or name == 'FULL_CONTROL':
            permissions['read_acp'] = True
        if name == 'WRITE_ACP' or name == 'FULL_CONTROL':
            permissions['write_acp'] = True
        
    @staticmethod
    def _s3_group_to_string(uri):
        if uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
            return 'Authenticated users'
        elif uri == 'http://acs.amazonaws.com/groups/global/AllUsers':
            return 'Everyone'
        elif uri == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
            return 'Log delivery'
        else:
            return uri

    @staticmethod
    def _status_to_bool(value):
        """ Converts a string to True if it is equal to 'Enabled' or to False otherwise. """
        return value == 'Enabled'

