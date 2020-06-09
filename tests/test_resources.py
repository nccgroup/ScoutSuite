import unittest
from ScoutSuite.providers.base.resources.base import (
    Resources, CompositeResources)
import asyncio
import json
import os


class DummyResources(Resources):
    def __init__(self, facade, region: str, some_other_scope: str,  **kwargs):
        self.region = region
        self.some_other_scope = some_other_scope

    async def fetch_all(self):
        self['resource_a'] = {
            'some_id': 1, 'region': self.region, 'some_other_scope': self.some_other_scope}
        self['resource_b'] = {
            'some_id': 2, 'region': self.region, 'some_other_scope': self.some_other_scope}


class DummyComposite(CompositeResources):
    _children = [
        (DummyResources, 'some_dummy_resources'),
        (DummyResources, 'other_dummy_resources')
    ]

    def __init__(self):
        self.facade = None

    async def fetch_all(self):
        for key in range(2):
            self[str(key)] = {}

        for key in self:
            await self._fetch_children(self[key], {
                'region': 'some_region',
                'some_other_scope': key
            })


class TestResources(unittest.TestCase):
    test_dir = os.path.dirname(os.path.realpath(__file__))

    def test_composite_resource(self):
        loop = asyncio.new_event_loop()
        composite = DummyComposite()
        loop.run_until_complete(composite.fetch_all())

        with open(os.path.join(self.test_dir, 'data/resources/dummy_resources.json')) as f:
            expected_object = json.load(f)

        expected_json = json.dumps(expected_object)
        actual_json = json.dumps(composite)
        print(actual_json)
        assert (expected_json == actual_json)
