from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Contacts(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_contacts = await self.facade.essentialcontacts.get_contacts(self.project_id)

        for raw_contact in raw_contacts:
            contact_id = get_non_provider_id(raw_contact['name'])
            raw_contact['id'] = contact_id
            self[contact_id] = raw_contact
