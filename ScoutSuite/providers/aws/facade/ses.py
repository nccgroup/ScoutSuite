from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade

import asyncio


class SESFacade(AWSBaseFacade):
    async def get_identities(self, region: str):
        identity_names = await AWSFacadeUtils.get_all_pages('ses', region, self.session, 'list_identities', 'Identities')
        identities = []
        # Fetch dkim attributes concurrently:
        tasks = {
            asyncio.ensure_future(
                self.get_identity_dkim_attributes(region, identity_name)
            ) for identity_name in identity_names
        }
        for result in asyncio.as_completed(tasks):
            identity_name, dkim_attributes = await result
            identities.append((identity_name, dkim_attributes))

        return identities

    async def get_identity_dkim_attributes(self, region: str, identity_name: str):
        ses_client = AWSFacadeUtils.get_client('ses', region, self.session)
        dkim_attributes = await run_concurrently(
            lambda: ses_client.get_identity_dkim_attributes(Identities=[identity_name])['DkimAttributes'][identity_name]
        )
        return identity_name, dkim_attributes

    async def get_identity_policies(self, region: str, identity_name: str):
        ses_client = AWSFacadeUtils.get_client('ses', region, self.session)
        policy_names = await run_concurrently(
            lambda: ses_client.list_identity_policies(Identity=identity_name)['PolicyNames']
        )

        if len(policy_names) == 0:
            return {}

        return await run_concurrently(
            lambda: ses_client.get_identity_policies(Identity=identity_name, PolicyNames=policy_names)['Policies']
        )
