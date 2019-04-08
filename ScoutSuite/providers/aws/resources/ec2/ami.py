from ScoutSuite.providers.aws.resources.base import AWSResources


class AmazonMachineImages(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_images = await self.facade.ec2.get_images(self.scope['region'], self.scope['owner_id'])
        if raw_images:
            for raw_image in raw_images:
                name, resource = self._parse_image(raw_image)
                self[name] = resource

    def _parse_image(self, raw_image):
        raw_image['id'] = raw_image['ImageId']
        raw_image['name'] = raw_image['Name']

        return raw_image['id'], raw_image
