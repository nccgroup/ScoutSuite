from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Contacts(AWSResources):
    def __init__(self, facade: AWSFacade):
        super().__init__(facade)
        self.partition = facade.partition
        self.service = 'account'
        self.resource_type = 'contact'

    async def fetch_all(self):
        # These settings are associated directly with the service, not with any resource. 
        # However, ScoutSuite seems to assume that every setting is tied to a resource so we make 
        # up a fake resource to hold them.
        self[0] = {}
        self[0]['contact_information'] = (await self.facade.account.get_contact_information())['ContactInformation']
        self[0]['security_contact'] = (await self.facade.account.get_alternate_contact(contact_type="SECURITY"))['AlternateContact']
