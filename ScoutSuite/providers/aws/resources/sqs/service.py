import json

from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources


class RegionalQueues(AWSResources):
    async def fetch_all(self, **kwargs):
        queue_urls = await self.facade.sqs.get_queues(self.scope['region'])
        # TODO: parallelize this async loop:
        for queue_url in queue_urls:
            id, queue = await self._parse_queue(queue_url)
            self[id] = queue

    async def _parse_queue(self, queue_url):
        queue = {'QueueUrl': queue_url}
        attributes = await self.facade.sqs.get_queue_attributes(
            self.scope['region'], queue_url, ['CreatedTimestamp', 'Policy', 'QueueArn', 'KmsMasterKeyId']
        )
        queue['arn'] = attributes.pop('QueueArn')
        queue['name'] = queue['arn'].split(':')[-1]
        queue['kms_master_key_id'] = attributes.pop('KmsMasterKeyId', None)
        queue['CreatedTimestamp'] = attributes.pop('CreatedTimestamp', None)

        if 'Policy' in attributes:
            queue['Policy'] = json.loads(attributes['Policy'])
        else:
            queue['Policy'] = {'Statement': []}

        return queue['name'], queue


class SQS(Regions):
    _children = [
        (RegionalQueues, 'queues')
    ]

    def __init__(self):
        super(SQS, self).__init__('sqs')
