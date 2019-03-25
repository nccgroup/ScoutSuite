from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently

import asyncio


class SNSFacade(AWSBaseFacade):
    regional_subscriptions_cache_locks = {}
    subscriptions_cache = {}

    async def get_topics(self, region: str):
        topics = await AWSFacadeUtils.get_all_pages('sns', region, self.session, 'list_topics', 'Topics')

        if len(topics) == 0:
            return []

        # Fetch and set the attributes of all topics concurrently:
        tasks = {
            asyncio.ensure_future(
                self.get_and_set_topic_attributes(region, topic)
            ) for topic in topics
        }
        await asyncio.wait(tasks)

        return topics

    async def get_and_set_topic_attributes(self, region: str, topic: {}):
        sns_client = AWSFacadeUtils.get_client('sns', region, self.session)
        topic['attributes'] = await run_concurrently(
            lambda: sns_client.get_topic_attributes(TopicArn=topic['TopicArn'])['Attributes']
        )

    async def get_subscriptions(self, region: str, topic_name: str):
        await self.cache_subscriptions(region)
        return [subscription for subscription in self.subscriptions_cache[region]
                if subscription['topic_name'] == topic_name]

    async def cache_subscriptions(self, region: str):
        async with self.regional_subscriptions_cache_locks.setdefault(region, asyncio.Lock()):
            if region in self.subscriptions_cache:
                return

            self.subscriptions_cache[region] =\
                await AWSFacadeUtils.get_all_pages('sns', region, self.session, 'list_subscriptions', 'Subscriptions')

            for subscription in self.subscriptions_cache[region]:
                topic_arn = subscription.pop('TopicArn')
                subscription['topic_name'] = topic_arn.split(':')[-1]
