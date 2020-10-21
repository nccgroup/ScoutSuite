from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.core.console import print_exception


class AmazonMachineImages(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_images = await self.facade.ec2.get_images(self.region)
        for raw_image in raw_images:
            try:
                name, resource = self._parse_image(raw_image)
                self[name] = resource
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_image(self, raw_image):
        raw_image['id'] = raw_image.get('ImageId')
        raw_image['name'] = raw_image.get('Name')
        raw_image['arn'] = 'arn:aws:ec2:{}:{}:ami/{}'.format(self.region,
                                                            raw_image.get('OwnerId'),
                                                            raw_image.get('ImageId'))
        return raw_image['id'], raw_image
