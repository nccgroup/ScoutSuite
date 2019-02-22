from ScoutSuite.providers.aws.configs.regions_config import ScopedResources
from ScoutSuite.providers.aws.facade import AWSFacade

class AmazonMachineImages(ScopedResources):
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.facade = AWSFacade()
    
    async def get_resources_in_scope(self, region): 
        return self.facade.get_ec2_images(region, self.owner_id)

    def parse_resource(self, raw_image):
        raw_image['id'] = raw_image['ImageId']
        raw_image['name'] = raw_image['Name']

        return raw_image['id'], raw_image
