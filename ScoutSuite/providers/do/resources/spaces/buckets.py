from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade
import json


class Buckets(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):

        buckets = await self.facade.spaces.get_all_buckets()
        if buckets:
            for bucket in buckets:
                id, bucket = await self._parse_buckets(bucket)
                self[id] = bucket

    async def _parse_buckets(self, raw_buckets):
        buckets_dict = {}

        buckets_dict["name"] = raw_buckets["Name"]
        buckets_dict["public_read"] = (
            str(raw_buckets["grantees"]["AllUsers"]["permissions"]["read"])
            if raw_buckets["grantees"]
            else None
        )
        buckets_dict["public_write"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["write"]
            if raw_buckets["grantees"]
            else None
        )
        buckets_dict["read_acp"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["read_acp"]
            if raw_buckets["grantees"]
            else None
        )
        buckets_dict["write_acp"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["write_acp"]
            if raw_buckets["grantees"]
            else None
        )

        return buckets_dict["name"], buckets_dict
