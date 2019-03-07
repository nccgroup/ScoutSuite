from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class CloudTrailFacade:
    async def get_trails(self, region):
        client = AWSFacadeUtils.get_client('cloudtrail', region)
        trails = await run_concurrently(
            lambda: client.describe_trails()['trailList']
        )

        for trail in trails:
            trail.update(await run_concurrently(
                lambda: client.get_trail_status(Name=trail['TrailARN'])
            ))
            trail['EventSelectors'] = await run_concurrently(
                lambda: client.get_event_selectors(TrailName=trail['TrailARN'])['EventSelectors']
            )

        return trails
