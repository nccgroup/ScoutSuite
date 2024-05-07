from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade
from ScoutSuite.core.console import print_exception
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
            if "AllUsers" in raw_buckets.get("grantees", {})
            else False
        )
        buckets_dict["public_write"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["write"]
            if "AllUsers" in raw_buckets.get("grantees", {})
            else False
        )
        buckets_dict["read_acp"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["read_acp"]
            if "AllUsers" in raw_buckets.get("grantees", {})
            else False
        )
        buckets_dict["write_acp"] = (
            raw_buckets["grantees"]["AllUsers"]["permissions"]["write_acp"]
            if "AllUsers" in raw_buckets.get("grantees", {})
            else False
        )
        buckets_dict["CORS"] = (
            True
            if "CORS" in raw_buckets and raw_buckets["CORS"] and "AllowedOrigins" in raw_buckets["CORS"][0]
            else False
        )        
        return buckets_dict["name"], buckets_dict