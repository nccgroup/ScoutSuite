from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils

class EssentialContactsFacade(GCPBaseFacade):
    def __init__(self):
        super().__init__('essentialcontacts', 'v1')  # API Client

    async def get_contacts(self, project_id: str):
        try:
            essentialcontacts_client = self._get_client()
            contacts = essentialcontacts_client.projects().contacts()
            request = contacts.list(parent=f"projects/{project_id}")
            results = await GCPFacadeUtils.get_all('contacts', request, contacts)
            return results
        except Exception as e:
            print_exception(f'Failed to list Essential Contacts: {e}')
            return []