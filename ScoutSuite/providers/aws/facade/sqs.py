from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

import asyncio


class SQSFacade(AWSBaseFacade):
    async def get_queues(self, region: str, attribute_names: []):
        sqs_client = AWSFacadeUtils.get_client('sqs', self.session, region)
        raw_queues = await run_concurrently(sqs_client.list_queues)

        if 'QueueUrls' not in raw_queues:
            return []

        queue_urls = raw_queues['QueueUrls']
        # Fetch the attributes of all the queues concurrently::
        tasks = {
            asyncio.ensure_future(
                self.get_queue_attributes(region, queue_url, attribute_names)
            ) for queue_url in queue_urls
        }
        queues = []
        for result in asyncio.as_completed(tasks):
            queue_url, queue_attributes = await result
            queues.append((queue_url, queue_attributes))

        return queues

    async def get_queue_attributes(self, region: str, queue_url: str, attribute_names: []):
        sqs_client = AWSFacadeUtils.get_client('sqs', self.session, region)
        queue_attributes = await run_concurrently(
            lambda: sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=attribute_names)['Attributes']
        )

        return queue_url, queue_attributes
