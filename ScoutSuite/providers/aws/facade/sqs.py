from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class SQSFacade(AWSBaseFacade):
    async def get_queues(self, region: str):
        sqs_client = AWSFacadeUtils.get_client('sqs', region, self.session)
        queues = await run_concurrently(sqs_client.list_queues)

        if 'QueueUrls' in queues:
            return queues['QueueUrls']

        return []

    async def get_queue_attributes(self, region: str, queue_url: str, attribute_names: []):
        sqs_client = AWSFacadeUtils.get_client('sqs', region, self.session)
        return await run_concurrently(
            lambda: sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=attribute_names)['Attributes']
        )
