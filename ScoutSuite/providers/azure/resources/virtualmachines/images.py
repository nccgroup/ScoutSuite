from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class Images(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_image in await self.facade.virtualmachines.get_images(self.subscription_id):
            try:
                id, image = self._parse_image(raw_image)
                self[id] = image
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_image(self, raw_image):
        image_dict = {}
        image_dict['id'] = get_non_provider_id(raw_image.id)
        image_dict['name'] = raw_image.name
        image_dict['type'] = raw_image.type
        image_dict['location'] = raw_image.location
        image_dict['tags'] = raw_image.tags
        image_dict['source_virtual_machine'] = raw_image.source_virtual_machine
        image_dict['storage_profile'] = raw_image.storage_profile
        image_dict['provisioning_state'] = raw_image.provisioning_state
        image_dict['hyper_vgeneration'] = raw_image.hyper_vgeneration
        image_dict['additional_properties'] = raw_image.additional_properties
        return image_dict['id'], image_dict


