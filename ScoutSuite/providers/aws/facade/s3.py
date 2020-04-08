import json

from botocore.exceptions import ClientError

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently


class S3Facade(AWSBaseFacade):
    async def get_buckets(self):
        client = AWSFacadeUtils.get_client('s3', self.session)
        try:
            buckets = await run_concurrently(lambda: client.list_buckets()['Buckets'])
        except Exception as e:
            print_exception('Failed to list buckets: {}'.format(e))
            return []
        else:
            # We need first to retrieve bucket locations before retrieving bucket details:
            await get_and_set_concurrently([self._get_and_set_s3_bucket_location], buckets)

            # Then we can retrieve bucket details concurrently:
            await get_and_set_concurrently(
                [self._get_and_set_s3_bucket_logging,
                 self._get_and_set_s3_bucket_versioning,
                 self._get_and_set_s3_bucket_webhosting,
                 self._get_and_set_s3_bucket_default_encryption,
                 self._get_and_set_s3_acls,
                 self._get_and_set_s3_bucket_policy,
                 self._get_and_set_s3_bucket_tags],
                buckets)

            # Non-async post-processing:
            for bucket in buckets:
                self._set_s3_bucket_secure_transport(bucket)

            return buckets

    async def _get_and_set_s3_bucket_location(self, bucket: {}):
        client = AWSFacadeUtils.get_client('s3', self.session)
        try:
            location = await run_concurrently(lambda: client.get_bucket_location(Bucket=bucket['Name']))
        except Exception as e:
            print_exception('Failed to get bucket location for {}: {}'.format(bucket['Name'], e))
            location = None

        if location:
            region = location['LocationConstraint'] if location['LocationConstraint'] else 'us-east-1'

            # Fixes issue #59: location constraint can be either EU or eu-west-1 for Ireland...
            if region == 'EU':
                region = 'eu-west-1'
        else:
            region = None

        bucket['region'] = region

    async def _get_and_set_s3_bucket_logging(self, bucket):
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'], )
        try:
            logging = await run_concurrently(lambda: client.get_bucket_logging(Bucket=bucket['Name']))
        except Exception as e:
            print_exception('Failed to get logging configuration for %s: %s' % (bucket['Name'], e))
            bucket['logging'] = 'Unknown'
        else:
            if 'LoggingEnabled' in logging:
                bucket['logging'] = \
                    logging['LoggingEnabled']['TargetBucket'] + '/' + logging['LoggingEnabled']['TargetPrefix']
            else:
                bucket['logging'] = 'Disabled'

    async def _get_and_set_s3_bucket_versioning(self, bucket):
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            versioning = await run_concurrently(lambda: client.get_bucket_versioning(Bucket=bucket['Name']))
            bucket['versioning_status_enabled'] = self._status_to_bool(versioning.get('Status'))
            bucket['version_mfa_delete_enabled'] = self._status_to_bool(versioning.get('MFADelete'))
        except Exception as e:
            print_exception('Failed to get versioning configuration for %s: %s' % (bucket['Name'], e))
            bucket['versioning_status_enabled'] = None
            bucket['version_mfa_delete_enabled'] = None

    async def _get_and_set_s3_bucket_webhosting(self, bucket):
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            result = await run_concurrently(lambda: client.get_bucket_website(Bucket=bucket['Name']))
            bucket['web_hosting_enabled'] = 'IndexDocument' in result
        except Exception as e:
            if "NoSuchWebsiteConfiguration" in str(e):
                bucket['web_hosting_enabled'] = False
            else:
                print_exception('Failed to get web hosting configuration for %s: %s' % (bucket['Name'], e))

    async def _get_and_set_s3_bucket_default_encryption(self, bucket):
        bucket_name = bucket['Name']
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            await run_concurrently(lambda: client.get_bucket_encryption(Bucket=bucket['Name']))
            bucket['default_encryption_enabled'] = True
        except ClientError as e:
            if 'ServerSideEncryptionConfigurationNotFoundError' in e.response['Error']['Code']:
                bucket['default_encryption_enabled'] = False
            else:
                bucket['default_encryption_enabled'] = None
                print_exception('Failed to get encryption configuration for %s: %s' % (bucket_name, e))
        except Exception as e:
            print_exception('Failed to get encryption configuration for %s: %s' % (bucket_name, e))
            bucket['default_encryption'] = 'Unknown'

    async def _get_and_set_s3_acls(self, bucket, key_name=None):
        bucket_name = bucket['Name']
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            grantees = {}
            if key_name:
                grants = await run_concurrently(lambda: client.get_object_acl(Bucket=bucket_name, Key=key_name))
            else:
                grants = await run_concurrently(lambda: client.get_bucket_acl(Bucket=bucket_name))
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
            print_exception('Failed to get ACL configuration for %s: %s' % (bucket_name, e))
            bucket['grantees'] = {}

    async def _get_and_set_s3_bucket_policy(self, bucket):
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            bucket_policy = await run_concurrently(lambda: client.get_bucket_policy(Bucket=bucket['Name']))
            bucket['policy'] = json.loads(bucket_policy['Policy'])
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
                print_exception('Failed to get bucket policy for %s: %s' % (bucket['Name'], e))
        except Exception as e:
            print_exception('Failed to get bucket policy for %s: %s' % (bucket['Name'], e))
            bucket['grantees'] = {}

    async def _get_and_set_s3_bucket_tags(self, bucket):
        client = AWSFacadeUtils.get_client('s3', self.session, bucket['region'])
        try:
            bucket_tagset = await run_concurrently(lambda: client.get_bucket_tagging(Bucket=bucket['Name']))
            bucket['tags'] = {x['Key']: x['Value'] for x in bucket_tagset['TagSet']}
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchTagSet':
                print_exception('Failed to get bucket tags for %s: %s' % (bucket['Name'], e))
        except Exception as e:
            print_exception('Failed to get bucket tags for %s: %s' % (bucket['Name'], e))
            bucket['tags'] = {}

    def _set_s3_bucket_secure_transport(self, bucket):
        try:
            if 'policy' in bucket:
                bucket['secure_transport_enabled'] = False
                for statement in bucket['policy']['Statement']:
                    # evaluate statement to see if it contains a condition disallowing HTTP transport
                    # TODO this might not cover all cases
                    if 'Condition' in statement and \
                            'Bool' in statement['Condition'] and \
                            'aws:SecureTransport' in statement['Condition']['Bool'] and \
                            ((statement['Condition']['Bool']['aws:SecureTransport'] == 'false' and
                              statement['Effect'] == 'Deny') or
                             (statement['Condition']['Bool']['aws:SecureTransport'] == 'true' and
                              statement['Effect'] == 'Allow')):
                        bucket['secure_transport_enabled'] = True
            else:
                bucket['secure_transport_enabled'] = False
        except Exception as e:
            print_exception('Failed to evaluate bucket policy for %s: %s' % (bucket['Name'], e))
            bucket['secure_transport'] = None

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
