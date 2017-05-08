# -*- coding: utf-8 -*-
"""
CloudWatch-related classes and functions
"""

# Import AWSScout2
from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# CloudWatchRegionConfig
########################################

class CloudWatchRegionConfig(RegionConfig):
    """
    CloudWatch configuration for a single AWS region

    :ivar trails:                       Dictionary of trails [name]
    :ivar trails_count:                 Number of trails in the region
    """

    def __init__(self):
        self.alarms = {}
        self.alarms_count = 0
        self.metrics = {}


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
        for k in ['AlarmConfigurationUpdatedTimestamp', 'StateReason', 'StateReasonData', 'Statistic', 'ComparisonOperator', 'Threshold', 'StateUpdatedTimestamp']:
            foo = alarm.pop(k) if k in alarm else None
        alarm_id = self.get_non_aws_id(alarm['arn'])
        metric_id = self.get_non_aws_id('%s/%s' % (alarm['Namespace'], alarm['MetricName']))
        self.alarms[alarm_id] = alarm
        #self.metrics[me]
        #manage_dictionary(metrics, metric_id, {'name': alarm['MetricName'], 'namespace': alarm['Namespace']})



########################################
# CloudWatchConfig
########################################

class CloudWatchConfig(RegionalServiceConfig):
    """
    CloudWatch configuration for all AWS regions

    :cvar targets:                      Tuple with all CloudWatch resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('alarms', 'MetricAlarms', 'describe_alarms', False),
    )
    region_config_class = CloudWatchRegionConfig
