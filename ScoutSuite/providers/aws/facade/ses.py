from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import map_concurrently


class SESFacade(AWSBaseFacade):
    async def get_identities(self, region: str):
        identity_names = await AWSFacadeUtils.get_all_pages(
            'ses', region, self.session, 'list_identities', 'Identities')

        return await map_concurrently(self._get_identity_dkim_attributes, identity_names, region=region)

    async def _get_identity_dkim_attributes(self, identity_name: str, region: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        dkim_attributes = await run_concurrently(
            lambda: ses_client.get_identity_dkim_attributes(Identities=[identity_name])['DkimAttributes'][identity_name]
        )
        return identity_name, dkim_attributes

    async def get_identity_policies(self, region: str, identity_name: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        policy_names = await run_concurrently(
            lambda: ses_client.list_identity_policies(Identity=identity_name)['PolicyNames']
        )

        if len(policy_names) == 0:
            return {}

        return await run_concurrently(
            lambda: ses_client.get_identity_policies(Identity=identity_name, PolicyNames=policy_names)['Policies']
        )
