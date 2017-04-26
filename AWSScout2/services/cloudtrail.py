# -*- coding: utf-8 -*-
"""
CloudTrail-related classes and functions
"""

# Import AWSScout2
from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# CloudTrailRegionConfig
########################################

class CloudTrailRegionConfig(RegionConfig):
    """
    CloudTrail configuration for a single AWS region

    :ivar trails:                       Dictionary of trails [name]
    :ivar trails_count:                 Number of trails in the region
    """

    def __init__(self):
        self.trails = {}
        self.trails_count = 0

    def parse_trail(self, global_params, region, trail):
        """
        Parse a single CloudTrail trail

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 Trail
        """
        trail_config = {}
        trail_config['name'] = trail.pop('Name')
        trail_id = self.get_non_aws_id(trail_config['name'])
        # Do not duplicate entries for multiregion trails
        if 'IsMultiRegionTrail' in trail and trail['IsMultiRegionTrail'] and trail['HomeRegion'] != region:
            for key in ['HomeRegion', 'TrailARN']:
                trail_config[key] = trail[key]
            trail_config['scout2_link'] = 'services.cloudtrail.regions.%s.trails.%s' % (trail['HomeRegion'], trail_id)
        else:
            for key in trail:
                trail_config[key] = trail[key]
            trail_config['bucket_id'] = self.get_non_aws_id(trail_config.pop('S3BucketName'))
            for key in ['IsMultiRegionTrail', 'LogFileValidationEnabled']:
                if key not in trail_config:
                    trail_config[key] = False
            trail_details = api_clients[region].get_trail_status(Name=trail['TrailARN'])
            for key in ['IsLogging', 'LatestDeliveryTime', 'LatestDeliveryError', 'StartLoggingTime', 'StopLoggingTime', 'LatestNotificationTime', 'LatestNotificationError', 'LatestCloudWatchLogsDeliveryError', 'LatestCloudWatchLogsDeliveryTime']:
                trail_config[key] = trail_details[key] if key in trail_details else None
        self.trails[trail_id] = trail_config



########################################
# CloudTrailConfig
########################################

class CloudTrailConfig(RegionalServiceConfig):
    """
    CloudTrail configuration for all AWS regions

    :cvar targets:                      Tuple with all CloudTrail resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('trails', 'trailList', 'describe_trails', False),
    )
    region_config_class = CloudTrailRegionConfig



########################################
# Post Processing
########################################

def cloudtrail_postprocessing(aws_config):
    cloudtrail_config = aws_config['services']['cloudtrail']
    # Global services logging duplicated
    if 'cloudtrail-duplicated-global-services-logging' in cloudtrail_config['violations']:
        if len(cloudtrail_config['violations']['cloudtrail-duplicated-global-services-logging']['items']) < 2:
            cloudtrail_config['violations']['cloudtrail-duplicated-global-services-logging']['items'] = []
            cloudtrail_config['violations']['cloudtrail-duplicated-global-services-logging']['flagged_items'] = 0
    # Global services logging disabled
    if 'cloudtrail-no-global-services-logging' in cloudtrail_config['violations']:
        if len(cloudtrail_config['violations']['cloudtrail-no-global-services-logging']['items']) != cloudtrail_config['violations']['cloudtrail-no-global-services-logging']['checked_items']:
            cloudtrail_config['violations']['cloudtrail-no-global-services-logging']['items'] = []
            cloudtrail_config['violations']['cloudtrail-no-global-services-logging']['flagged_items'] = 0
    # CloudTrail not enabled at all...
    if not sum(cloudtrail_config['regions'][r]['trails_count'] for r in cloudtrail_config['regions']):
        for r in cloudtrail_config['regions']:
            cloudtrail_config['violations']['cloudtrail-no-logging']['items'].append('cloudtrail.regions.%s' % r)
            cloudtrail_config['violations']['cloudtrail-no-logging']['checked_items'] += 1
            cloudtrail_config['violations']['cloudtrail-no-logging']['flagged_items'] += 1
            cloudtrail_config['violations']['cloudtrail-no-logging']['dashboard_name'] = 'Regions'
