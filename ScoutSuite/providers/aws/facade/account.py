from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class AccountFacade(AWSBaseFacade):
    async def get_contact_information(self):
        client = AWSFacadeUtils.get_client('account', self.session)
        try:
            contact_info = await run_concurrently(lambda: client.get_contact_information())
            return contact_info
        except Exception as e:
            print_exception(f'Failed to retrieve account contact details: {e}')

    async def get_alternate_contact(self, contact_type):
        client = AWSFacadeUtils.get_client('account', self.session)
        try:
            contact_info = await run_concurrently(lambda: client.get_alternate_contact(AlternateContactType=contact_type))
            return contact_info
        except client.exceptions.ResourceNotFoundException as e:
            # AWS throws if there is no contact of the requested type
            return {'AlternateContact': None}
        except Exception as e:
            print_exception(f'Failed to retrieve account alternate contact details: {e}')
