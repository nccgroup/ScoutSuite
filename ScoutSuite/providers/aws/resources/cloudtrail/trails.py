import time

from ScoutSuite.core.console import print_error
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Trails(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_trails = await self.facade.cloudtrail.get_trails(self.region)
        for raw_trail in raw_trails:
            name, resource = self._parse_trail(raw_trail)
            self[name] = resource

    def _parse_trail(self, raw_trail):
        try:
            # Initialize all required attributes with defaults
            trail = {
                'name': raw_trail.pop('Name', ''),
                'arn': raw_trail.get('TrailARN', ''),
                'is_organization_trail': raw_trail.get('IsOrganizationTrail', False),
                'home_region': raw_trail.get('HomeRegion', ''),
                'IsMultiRegionTrail': raw_trail.get('IsMultiRegionTrail', False),
                'IsLogging': raw_trail.get('IsLogging', False),
                'IncludeGlobalServiceEvents': raw_trail.get('IncludeGlobalServiceEvents', False),
                'EventSelectors': raw_trail.get('EventSelectors', []),
                'LogFileValidationEnabled': raw_trail.get('LogFileValidationEnabled', False)
            }
            
            trail_id = get_non_provider_id(trail['name'])
            if not trail_id:
                return None, None

            # Handle multiregion trails
            if trail['IsMultiRegionTrail'] and trail['home_region'] != self.region:
                trail['scout_link'] = f'services.cloudtrail.regions.{trail["home_region"]}.trails.{trail_id}'
                return trail_id, trail

            # Process remaining attributes
            if 'S3BucketName' in raw_trail:
                trail['bucket_id'] = get_non_provider_id(raw_trail['S3BucketName'])

            trail['wildcard_data_logging'] = self.data_logging_status(trail)

            return trail_id, trail

        except Exception as e:
            print_error(f'Failed to parse trail: {str(e)}')
            return None, None

    def data_logging_status(self, trail):
        for event_selector in trail.get('EventSelectors', []):
            has_wildcard = \
                {'Values': ['arn:aws:s3'], 'Type': 'AWS::S3::Object'} in event_selector['DataResources'] or \
                {'Values': ['arn:aws:lambda'], 'Type': 'AWS::Lambda::Function'} in event_selector['DataResources']
            is_logging = trail['IsLogging']
            if has_wildcard and is_logging and self.is_fresh(trail):
                return True
        return False

    @staticmethod
    def is_fresh(trail_details):
        if not trail_details:
            return False
            
        delivery_time = trail_details.get('LatestCloudWatchLogsDeliveryTime')
        if not delivery_time:
            return False
            
        try:
            delivery_time = delivery_time.strftime("%s")
            delivery_age = ((int(time.time()) - int(delivery_time)) / 1440)
            return delivery_age <= 24
        except Exception:
            return False
