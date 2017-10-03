# -*- coding: utf-8 -*-
"""
CloudWatch-related classes and functions
"""

from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig



########################################
# CloudWatchRegionConfig
########################################

class CloudWatchRegionConfig(RegionConfig):
    """
    CloudWatch configuration for a single AWS region
    """

    def parse_alarm(self, global_params, region, alarm):
        """
        Parse a single CloudWatch trail

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param alarm:                   Alarm
        """
        alarm['arn'] = alarm.pop('AlarmArn')
        alarm['name'] = alarm.pop('AlarmName')
        # Drop some data
        for k in ['AlarmConfigurationUpdatedTimestamp', 'StateReason', 'StateReasonData', 'StateUpdatedTimestamp']:
            foo = alarm.pop(k) if k in alarm else None
        alarm_id = self.get_non_aws_id(alarm['arn'])
        self.alarms[alarm_id] = alarm



########################################
# CloudWatchConfig
########################################

class CloudWatchConfig(RegionalServiceConfig):
    """
    CloudWatch configuration for all AWS regions
    """

    region_config_class = CloudWatchRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(CloudWatchConfig, self).__init__(service_metadata, thread_config)
