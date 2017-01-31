# -*- coding: utf-8 -*-
"""
SQS-related classes and functions
"""

# Import AWSScout2
from AWSScout2.configs import RegionalServiceConfig, RegionConfig, api_clients

# Import stock packages
import json



########################################
# SQSConfig
########################################

class SQSConfig(RegionalServiceConfig):
    """
    SQS configuration for all AWS regions

    :cvar targets:                      Tuple with all SQS resource names that may be fetched
    """
    targets = ('Queues')

    def init_region_config(self, region):
        """
        Initialize the region's configuration

        :param region:                  Name of the region
        """
        self.regions[region] = SQSRegionConfig()



########################################
# SQSRegionConfig
########################################

class SQSRegionConfig(RegionConfig):
    """
    SQS configuration for a single AWS region

    :ivar queues:                       Dictionary of queues [name]
    :ivar queues_count:                 Number of queues in the region
    """

    def __init__(self):
        self.queues = {}
        self.queues_count = 0


    def _fetch_queue(self, global_params, region, queue_url):
        """
        Parse a single queue and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param queue_url:               URL of the AWS queue
        """
        queue = {'QueueUrl': queue_url}
        attributes = api_clients[region].get_queue_attributes(QueueUrl = queue_url, AttributeNames = ['CreatedTimestamp', 'Policy', 'QueueArn'])['Attributes']
        queue['arn'] = attributes.pop('QueueArn')
        for k in ['CreatedTimestamp']:
            queue[k] = attributes[k] if k in attributes else None
        for k in ['Policy']:
            queue[k] = json.loads(attributes[k]) if k in attributes else None
        queue['name'] = queue['arn'].split(':')[-1]
        self.queues[queue['name']] = queue