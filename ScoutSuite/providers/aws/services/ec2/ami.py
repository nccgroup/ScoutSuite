from ScoutSuite.providers.aws.resources.resources import AWSSimpleResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class AmazonMachineImages(AWSSimpleResources):
    async def get_resources_from_api(self):
        return self.facade.ec2.get_images(self.scope['region'], self.scope['owner_id'])

    def parse_resource(self, raw_image):
        raw_image['id'] = raw_image['ImageId']
        raw_image['name'] = raw_image['Name']

        return raw_image['id'], raw_image
