import boto3

from ScoutSuite.providers.utils import run_concurrently


# TODO: Add docstrings
class AWSFacadeUtils:
    _clients = {}

    @staticmethod
    async def get_all_pages(service: str, region: str, session: boto3.session.Session, paginator_name: str, entity: str, **paginator_args):
        results = await AWSFacadeUtils.get_multiple_entities_from_all_pages(service, region, session, paginator_name, [entity], **paginator_args)
        return results[entity]

    @staticmethod
    async def get_multiple_entities_from_all_pages(service: str, region: str, session: boto3.session.Session, paginator_name: str, entities: list, **paginator_args):
        client = AWSFacadeUtils.get_client(service, session, region)

        # Building a paginator doesn't require any API call so no need to do it concurrently:
        paginator = client.get_paginator(
            paginator_name).paginate(**paginator_args)

        # Getting all pages from a paginator requires API calls so we need to do it concurrently:
        return await run_concurrently(lambda: AWSFacadeUtils._get_all_pages_from_paginator(paginator, entities))

    @staticmethod
    def _get_all_pages_from_paginator(paginator, entities: list):
        resources = {entity: [] for entity in entities}

        # There's an API call hidden behind each iteration:
        for page in paginator:
            for entity in entities:
                resources[entity].extend(page[entity])

        return resources

    @staticmethod
    def get_client(service: str, session: boto3.session.Session, region: str=None):
        """
        Instantiates an AWS API client

        :param service:                         Service targeted, e.g. ec2
        :param session:                         The aws session
        :param region:                          Region desired, e.g. us-east-2

        :return:
        """

        # TODO: investigate the use of a mutex to avoid useless creation of a same type of client among threads:
        client = session.client(service, region_name=region) if region is not None else session.client(service)
        return AWSFacadeUtils._clients.setdefault((service, region), client)
