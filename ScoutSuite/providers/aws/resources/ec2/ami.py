from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class AmazonMachineImages(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, owner_id: str):
        self.region = region
        self.owner_id = owner_id

        super(AmazonMachineImages, self).__init__(facade)

    async def fetch_all(self, **kwargs):
        raw_images = await self.facade.ec2.get_images(self.region, self.owner_id)
        for raw_image in raw_images:
            name, resource = self._parse_image(raw_image)
            self[name] = resource

    def _parse_image(self, raw_image):
        raw_image['id'] = raw_image['ImageId']
        raw_image['name'] = raw_image['Name']

        return raw_image['id'], raw_image
