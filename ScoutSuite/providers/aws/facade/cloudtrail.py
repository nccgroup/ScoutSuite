from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class CloudTrailFacade(AWSBaseFacade):
    async def get_trails(self, region):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        trails = await run_concurrently(
            lambda: client.describe_trails()['trailList'])
        await AWSFacadeUtils.get_and_set_concurrently(
            [self._get_and_set_status, self._get_and_set_selectors], trails, region=region)

        return trails

    async def _get_and_set_status(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        trail_status = await run_concurrently(
            lambda: client.get_trail_status(Name=trail['TrailARN']))
        trail.update(trail_status)

    async def _get_and_set_selectors(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        trail['EventSelectors'] = await run_concurrently(
            lambda: client.get_event_selectors(TrailName=trail['TrailARN'])['EventSelectors'])
