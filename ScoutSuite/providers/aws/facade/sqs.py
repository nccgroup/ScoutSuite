from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, map_concurrently


class SQSFacade(AWSBaseFacade):
    async def get_queues(self, region: str, attribute_names: []):
        sqs_client = AWSFacadeUtils.get_client('sqs', self.session, region)
        try:
            raw_queues = await run_concurrently(sqs_client.list_queues)
        except Exception as e:
            print_exception('Failed to list SQS queues: {}'.format(e))
            return []
        else:
            if 'QueueUrls' not in raw_queues:
                return []
            queue_urls = raw_queues['QueueUrls']

            return await map_concurrently(
                self._get_queue_attributes, queue_urls, region=region, attribute_names=attribute_names)

    async def _get_queue_attributes(self, queue_url: str, region: str, attribute_names: []):
        sqs_client = AWSFacadeUtils.get_client('sqs', self.session, region)
        try:
            queue_attributes = await run_concurrently(
                lambda: sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=attribute_names)[
                    'Attributes']
            )
        except Exception as e:
            print_exception('Failed to get SQS queue attributes: {}'.format(e))
            raise

        return queue_url, queue_attributes
