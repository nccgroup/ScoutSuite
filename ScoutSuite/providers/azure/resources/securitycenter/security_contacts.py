from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class SecurityContacts(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_contact in await self.facade.securitycenter.get_security_contacts(self.subscription_id):
            try:
                id, security_contact = self._parse_security_contact(raw_contact)
                self[id] = security_contact
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_security_contact(self, security_contact):
        security_contact_dict = {}
        security_contact_dict['id'] = security_contact.id
        security_contact_dict['name'] = security_contact.name
        security_contact_dict['email'] = security_contact.email
        security_contact_dict['phone'] = security_contact.phone
        security_contact_dict['alert_notifications'] = security_contact.alert_notifications == "On"
        security_contact_dict['alerts_to_admins'] = security_contact.alerts_to_admins == "On"
        security_contact_dict['additional_properties'] = security_contact.additional_properties

        return security_contact_dict['id'], security_contact_dict
