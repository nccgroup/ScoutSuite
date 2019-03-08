from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class DirectConnectFacade:
    async def get_connections(self, region):
        client = AWSFacadeUtils.get_client('directconnect', region)
        return await run_concurrently(
                lambda: client.describe_connections()['connections']
        )
