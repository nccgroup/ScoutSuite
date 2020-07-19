from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .buckets import Buckets


class S3(AWSCompositeResources):
    _children = [
        (Buckets, 'buckets')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__(facade)
        self.service = 's3'

    async def fetch_all(self, partition_name='aws', **kwargs):
        # Keep track of regions as S3 is both a global and regional service
        self.facade.s3.regions = kwargs.get('regions')
        self['public_access_block_configuration'] = self.facade.s3.get_s3_public_access_block(self.facade.owner_id)
        await self._fetch_children(self)

    async def finalize(self):
        for bucket_id in self['buckets']:
            if "public_access_block_configuration" in self['buckets'][bucket_id]:
                # The resulting configuration will be the most restrictive
                self['buckets'][bucket_id]["public_access_block_configuration"]["BlockPublicAcls"] = \
                self['buckets'][bucket_id]["public_access_block_configuration"]["BlockPublicAcls"] or \
                self['public_access_block_configuration']["BlockPublicAcls"]
                self['buckets'][bucket_id]["public_access_block_configuration"]["IgnorePublicAcls"] = \
                self['buckets'][bucket_id]["public_access_block_configuration"]["IgnorePublicAcls"] or \
                self['public_access_block_configuration']["IgnorePublicAcls"]
                self['buckets'][bucket_id]["public_access_block_configuration"]["BlockPublicPolicy"] = \
                self['buckets'][bucket_id]["public_access_block_configuration"]["BlockPublicPolicy"] or \
                self['public_access_block_configuration']["BlockPublicPolicy"]
                self['buckets'][bucket_id]["public_access_block_configuration"]["RestrictPublicBuckets"] = \
                self['buckets'][bucket_id]["public_access_block_configuration"]["RestrictPublicBuckets"] or \
                self['public_access_block_configuration']["RestrictPublicBuckets"]
            else:
                # No bucket-level configuration, use account level configuration
                self['buckets'][bucket_id]["public_access_block_configuration"] = self['public_access_block_configuration']
