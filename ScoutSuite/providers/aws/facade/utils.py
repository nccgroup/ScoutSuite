import boto3

from ScoutSuite.providers.utils import run_concurrently


# TODO: Add docstrings
class AWSFacadeUtils:
    _clients = {}

    @staticmethod
    async def get_all_pages(service: str, region: str, paginator_name: str, response_key: str, **paginator_args):
        client = await AWSFacadeUtils.get_client(service, region)
        pages = await run_concurrently(lambda: client.get_paginator(paginator_name).paginate(**paginator_args))

        return AWSFacadeUtils._get_from_all_pages(pages, response_key)

    @staticmethod
    def _get_from_all_pages(pages: [], key: str):
        resources = []
        for page in pages:
            resources.extend(page[key])

        return resources

    @staticmethod
    async def get_client(service: str, region: str):
        client = await run_concurrently(lambda: boto3.client(service, region_name=region))
        return AWSFacadeUtils._clients.setdefault((service, region), client)
