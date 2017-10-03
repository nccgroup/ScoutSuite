# -*- coding: utf-8 -*-
"""
SNS-related classes and functions
"""

import json

from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# SNSRegionConfig
########################################

class SNSRegionConfig(RegionConfig):
    """
    SNS configuration for a single AWS region
    """

    def parse_subscription(self, params, region, subscription):
        """
        Parse a single subscription and reference it in its corresponding topic

        :param params:                  Global parameters (defaults to {})
        :param subscription:            SNS Subscription
        """
        topic_arn = subscription.pop('TopicArn')
        topic_name = topic_arn.split(':')[-1]
        if topic_name in self.topics:
            topic = self.topics[topic_name]
            manage_dictionary(topic['subscriptions'], 'protocol', {})
            protocol = subscription.pop('Protocol')
            manage_dictionary(topic['subscriptions']['protocol'], protocol, [])
            topic['subscriptions']['protocol'][protocol].append(subscription)
            topic['subscriptions_count'] += 1


    def parse_topic(self, params, region, topic):
        """
        Parse a single topic and fetch additional attributes

        :param params:                  Global parameters (defaults to {})
        :param topic:                   SNS Topic
        """
        topic['arn'] = topic.pop('TopicArn')
        topic['name'] = topic['arn'].split(':')[-1]
        (prefix, partition, service, region, account, name) = topic['arn'].split(':')
        api_client = api_clients[region]
        attributes = api_client.get_topic_attributes(TopicArn=topic['arn'])['Attributes']
        for k in ['Owner', 'DisplayName']:
            topic[k] = attributes[k] if k in attributes else None
        for k in ['Policy', 'DeliveryPolicy', 'EffectiveDeliveryPolicy']:
            topic[k] = json.loads(attributes[k]) if k in attributes else None
        topic['name'] = topic['arn'].split(':')[-1]
        manage_dictionary(topic, 'subscriptions', {})
        manage_dictionary(topic, 'subscriptions_count', 0)
        self.topics[topic['name']] = topic



########################################
# SNSConfig
########################################

class SNSConfig(RegionalServiceConfig):
    """
    SNS configuration for all AWS regions
    """

    region_config_class = SNSRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(SNSConfig, self).__init__(service_metadata, thread_config)
