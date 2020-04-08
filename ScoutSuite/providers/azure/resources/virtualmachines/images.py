from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class Images(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Images, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_image in await self.facade.virtualmachines.get_images(self.subscription_id):
            id, image = self._parse_image(raw_image)
            self[id] = image

    def _parse_image(self, raw_image):
        # TODO
        pass
