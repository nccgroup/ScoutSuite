from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name, format_arn


class RegionalSettings(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region
        self.partition = facade.partition
        self.service = 'ec2'
        self.resource_type = 'regional_setting'

    async def fetch_all(self):
        self['ebs_encryption_default'] = await self.facade.ec2.get_ebs_encryption(self.region)
        self['ebs_default_encryption_key_id'] = await self.facade.ec2.get_ebs_default_encryption_key(self.region)
