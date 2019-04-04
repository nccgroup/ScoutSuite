from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class DirectConnectFacade(AWSBaseFacade):
    async def get_connections(self, region):
        client = AWSFacadeUtils.get_client('directconnect', self.session, region)
        return await run_concurrently(lambda: client.describe_connections()['connections'])
