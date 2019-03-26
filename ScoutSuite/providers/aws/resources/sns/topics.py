from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources

from .subscriptions import Subscriptions

import json


class Topics(AWSCompositeResources):
    _children = [
        (Subscriptions, 'subscriptions')
    ]

    async def fetch_all(self, **kwargs):
        raw_topics = await self.facade.sns.get_topics(self.scope['region'])
        # TODO: parallelize this async loop:
        for raw_topic in raw_topics:
            topic_name, topic = self._parse_topic(raw_topic)
            await self._fetch_children(
                parent=topic,
                scope={'region': self.scope['region'], 'topic_name': topic_name}
            )
            # Fix subscriptions count:
            topic['subscriptions_count'] = topic['subscriptions'].pop('subscriptions_count')
            self[topic_name] = topic

    def _parse_topic(self, raw_topic):
        raw_topic['arn'] = raw_topic.pop('TopicArn')
        raw_topic['name'] = raw_topic['arn'].split(':')[-1]

        attributes = raw_topic.pop('attributes')
        for k in ['Owner', 'DisplayName']:
            raw_topic[k] = attributes[k] if k in attributes else None
        for k in ['Policy', 'DeliveryPolicy', 'EffectiveDeliveryPolicy']:
            raw_topic[k] = json.loads(attributes[k]) if k in attributes else None

        return raw_topic['name'], raw_topic
