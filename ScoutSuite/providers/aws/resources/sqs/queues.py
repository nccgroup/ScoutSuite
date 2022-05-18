import json

from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Queues(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        queues = await self.facade.sqs.get_queues(self.region,
                                                  ['CreatedTimestamp', 'Policy', 'QueueArn', 'KmsMasterKeyId', 'SqsManagedSseEnabled'])
        for queue_url, queue_attributes in queues:
            id, queue = self._parse_queue(queue_url, queue_attributes)
            self[id] = queue

    def _parse_queue(self, queue_url, queue_attributes):
        queue = {}
        queue['arn'] = queue_attributes.get('QueueArn')
        queue['name'] = queue['arn'].split(':')[-1]
        queue['QueueUrl'] = queue_url
        queue['kms_master_key_id'] = queue_attributes.get('KmsMasterKeyId', None)
        queue['sqs_managed_sse_enabled'] = queue_attributes.pop('SqsManagedSseEnabled', None)
        queue['CreatedTimestamp'] = queue_attributes.get('CreatedTimestamp', None)

        if 'Policy' in queue_attributes:
            queue['Policy'] = json.loads(queue_attributes['Policy'])
        else:
            queue['Policy'] = {'Statement': []}

        return get_non_provider_id(queue['name']), queue
