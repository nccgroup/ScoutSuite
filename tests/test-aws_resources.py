from unittest import TestCase
from ScoutSuite.providers.aws.resources.resources import AWSResources, AWSCompositeResources
import asyncio
import json
import os 


class DummyResources(AWSResources):
    async def fetch_all(self):
        self['resource_a'] = {'some_id': 1, 'from_scope': self.scope}
        self['resource_b'] = {'some_id': 2, 'from_scope': self.scope}



class DummyComposite(AWSCompositeResources):
    _children = [
        (DummyResources, 'some_dummy_resources'),
        (DummyResources, 'other_dummy_resources')
    ]

    async def fetch_all(self, **kwargs):
        for key in range(2):
            self[str(key)] = {}

        for key in self:
            scope = {
                'region': self.scope['region'],
                'some_inner_scope': key
            }

            await self._fetch_children(resource_parent=self[key], scope=scope)


class TestAWSResources(TestCase):
    test_dir = os.path.dirname(os.path.realpath(__file__))

    def test_aws_composite_resource(self):
        loop = asyncio.new_event_loop()
        composite = DummyComposite(None, {'region': 'some_region'})
        loop.run_until_complete(composite.fetch_all())

        with open(os.path.join(self.test_dir, 'data/aws-resources/dummy_resources.json')) as f:
            expected_object = json.load(f)

        expected_json = json.dumps(expected_object)
        actual_json = json.dumps(composite)

        assert (expected_json == actual_json)
