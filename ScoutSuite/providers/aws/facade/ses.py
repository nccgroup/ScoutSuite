from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently
from ScoutSuite.providers.utils import run_concurrently


class SESFacade(AWSBaseFacade):
    async def get_identities(self, region: str):
        try:
            identity_names = await AWSFacadeUtils.get_all_pages(
                'ses', region, self.session, 'list_identities', 'Identities')

            return await map_concurrently(self._get_identity_dkim_attributes, identity_names, region=region)
        except Exception as e:
            print_exception(f'Failed to get SES identities: {e}')
            return []

    async def _get_identity_dkim_attributes(self, identity_name: str, region: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        try:
            dkim_attributes = await run_concurrently(
                lambda: ses_client.get_identity_dkim_attributes(Identities=[identity_name])['DkimAttributes'][
                    identity_name]
            )
        except Exception as e:
            print_exception(f'Failed to get SES DKIM attributes: {e}')
            raise
        return identity_name, dkim_attributes

    async def get_identity_policies(self, region: str, identity_name: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        try:
            policy_names = await run_concurrently(
                lambda: ses_client.list_identity_policies(Identity=identity_name)['PolicyNames']
            )
        except Exception as e:
            print_exception(f'Failed to list SES policies: {e}')
            policy_names = []

        if len(policy_names) == 0:
            return {}

        try:
            return await run_concurrently(
                lambda: ses_client.get_identity_policies(Identity=identity_name, PolicyNames=policy_names)['Policies']
            )
        except Exception as e:
            print_exception(f'Failed to get SES policies: {e}')
            return None
