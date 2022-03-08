import asyncio

from ScoutSuite.core.console import print_exception, print_warning
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently


class SNSFacade(AWSBaseFacade):
    regional_subscriptions_cache_locks = {}
    subscriptions_cache = {}

    async def get_topics(self, region: str):
        try:
            topics = await AWSFacadeUtils.get_all_pages('sns', region, self.session, 'list_topics', 'Topics')
            await get_and_set_concurrently([self._get_and_set_topic_attributes], topics, region=region)
        except Exception as e:
            print_exception(f'Failed to get CloudWatch alarms: {e}')
            topics = []
        finally:
            return topics

    async def _get_and_set_topic_attributes(self, topic: {}, region: str):
        sns_client = AWSFacadeUtils.get_client('sns', self.session, region)
        try:
            topic['attributes'] = await run_concurrently(
                lambda: sns_client.get_topic_attributes(TopicArn=topic['TopicArn'])['Attributes']
            )
        except Exception as e:
            if 'NotFound' in e:
                print_warning(f'Failed to get SNS topic attributes: {e}')
            else:
                print_exception(f'Failed to get SNS topic attributes: {e}')

    async def get_subscriptions(self, region: str, topic_name: str):
        await self.cache_subscriptions(region)
        return [subscription for subscription in self.subscriptions_cache[region]
                if subscription['topic_name'] == topic_name]

    async def cache_subscriptions(self, region: str):
        async with self.regional_subscriptions_cache_locks.setdefault(region, asyncio.Lock()):
            if region in self.subscriptions_cache:
                return

            self.subscriptions_cache[region] = \
                await AWSFacadeUtils.get_all_pages('sns', region, self.session, 'list_subscriptions', 'Subscriptions')

            for subscription in self.subscriptions_cache[region]:
                topic_arn = subscription.pop('TopicArn')
                subscription['topic_name'] = topic_arn.split(':')[-1]
