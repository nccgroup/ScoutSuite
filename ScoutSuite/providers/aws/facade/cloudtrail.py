from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import get_and_set_concurrently
from ScoutSuite.providers.utils import run_concurrently


class CloudTrailFacade(AWSBaseFacade):
    async def get_trails(self, region):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            trails = await run_concurrently(
                lambda: client.describe_trails()['trailList'])
        except Exception as e:
            print_exception(f'Failed to describe CloudTrail trail: {e}')
            trails = []
        else:
            await get_and_set_concurrently(
                [self._get_and_set_status, self._get_and_set_selectors], trails, region=region)
        finally:
            return trails

    async def _get_and_set_status(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            trail_status = await run_concurrently(
                lambda: client.get_trail_status(Name=trail['TrailARN']))
            trail.update(trail_status)
        except Exception as e:
            print_exception(f'Failed to get CloudTrail trail status: {e}')

    async def _get_and_set_selectors(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            # this call will fail for organization trails stored in another account
            trail['EventSelectors'] = await run_concurrently(
                lambda: client.get_event_selectors(TrailName=trail['TrailARN']).get('EventSelectors', []))
        except Exception as e:
            print_exception(f'Failed to get CloudTrail event selectors: {e}')
