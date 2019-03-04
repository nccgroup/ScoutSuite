from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudTrailFacade:
    def get_trails(self, region):
        client = AWSFacadeUtils.get_client('cloudtrail', region)
        trails = client.describe_trails()['trailList']

        for trail in trails:
            trail.update(client.get_trail_status(Name=trail['TrailARN']))
            trail['EventSelectors'] = client.get_event_selectors(TrailName=trail['TrailARN'])['EventSelectors']

        return trails