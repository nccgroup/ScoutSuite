# -*- coding: utf-8 -*-

import json

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# SQSRegionConfig
########################################

class SQSRegionConfig(RegionConfig):
    """
    SQS configuration for a single AWS region
    """

    def parse_queue(self, global_params, region, queue_url):
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
        if 'Policy' in attributes:
            queue['Policy'] = json.loads(attributes['Policy'])
        else:
            queue['Policy'] = {'Statement': []}

        queue['name'] = queue['arn'].split(':')[-1]
        self.queues[queue['name']] = queue



########################################
# SQSConfig
########################################

class SQSConfig(RegionalServiceConfig):
    """
    SQS configuration for all AWS regions
    """

    region_config_class = SQSRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(SQSConfig, self).__init__(service_metadata, thread_config)
