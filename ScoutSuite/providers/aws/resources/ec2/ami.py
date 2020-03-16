from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class AmazonMachineImages(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(AmazonMachineImages, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_images = await self.facade.ec2.get_images(self.region)
        for raw_image in raw_images:
            name, resource = self._parse_image(raw_image)
            self[name] = resource

    def _parse_image(self, raw_image):
        raw_image['id'] = raw_image.get('ImageId')
        raw_image['name'] = raw_image.get('Name')
        return raw_image['id'], raw_image
