import time

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Trails(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(Trails, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_trails = await self.facade.cloudtrail.get_trails(self.region)
        for raw_trail in raw_trails:
            name, resource = self._parse_trail(raw_trail)
            self[name] = resource

    def _parse_trail(self, raw_trail):
        trail = {'name': raw_trail.pop('Name')}
        trail_id = get_non_provider_id(trail['name'])

        # Do not duplicate entries for multiregion trails
        if 'IsMultiRegionTrail' in raw_trail and raw_trail['IsMultiRegionTrail'] and \
                raw_trail['HomeRegion'] != self.region:
            for key in ['HomeRegion', 'TrailARN']:
                trail[key] = raw_trail[key]
            trail['scout_link'] = 'services.cloudtrail.regions.%s.trails.%s' % (raw_trail['HomeRegion'], trail_id)
            return trail_id, trail

        for key in raw_trail:
            trail[key] = raw_trail[key]
        trail['bucket_id'] = get_non_provider_id(trail.pop('S3BucketName'))
        for key in ['IsMultiRegionTrail', 'LogFileValidationEnabled']:
            if key not in trail:
                trail[key] = False

        for key in ['KMSKeyId', 'IsLogging', 'LatestDeliveryTime', 'LatestDeliveryError', 'StartLoggingTime',
                    'StopLoggingTime', 'LatestNotificationTime', 'LatestNotificationError',
                    'LatestCloudWatchLogsDeliveryError', 'LatestCloudWatchLogsDeliveryTime']:
            trail[key] = trail[key] if key in trail else None

        # using trail ARN instead of name as with Organizations the trail would be located in another account
        trail['wildcard_data_logging'] = self.data_logging_status(trail)

        for event_selector in trail['EventSelectors']:
            trail['DataEventsEnabled'] = len(event_selector['DataResources']) > 0
            trail['ManagementEventsEnabled'] = event_selector['IncludeManagementEvents']

        return trail_id, trail

    def data_logging_status(self, trail):
        for event_selector in trail['EventSelectors']:
            has_wildcard = \
                {u'Values': ['arn:aws:s3'], 'Type': 'AWS::S3::Object'} in event_selector['DataResources'] or \
                {u'Values': ['arn:aws:lambda'], 'Type': 'AWS::Lambda::Function'} in event_selector['DataResources']
            is_logging = trail['IsLogging']
            if has_wildcard and is_logging and self.is_fresh(trail):
                return True
        return False

    @staticmethod
    def is_fresh(trail_details):
        if trail_details.get('LatestCloudWatchLogsDeliveryTime'):
            delivery_time = trail_details.get('LatestCloudWatchLogsDeliveryTime').strftime("%s")
            delivery_age = ((int(time.time()) - int(delivery_time)) / 1440)
            return delivery_age <= 24
        else:
            return False
