import boto3

from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials


# class OracleFacadeUtils:
#     _clients = {}
#
#     @staticmethod
#     async def get_all_pages(service: str, credentials: OracleCredentials, entity: str):
#
#         client = OracleFacadeUtils.get_client(service, credentials: OracleCredentials)
#
#         # Building a paginator doesn't require any API call so no need to do it concurrently:
#         paginator = client.get_paginator(paginator_name).paginate(**paginator_args)
#
#         # Getting all pages from a paginator requires API calls so we need to do it concurrently:
#         return await run_concurrently(lambda: AWSFacadeUtils._get_all_pages_from_paginator(paginator, entities))
#
#
#     @staticmethod
#     def get_client(service: str, session: boto3.session.Session, region: str = None):
#         """
#         Instantiates an OCI API client
#
#         """
#
#         return AWSFacadeUtils._clients.setdefault(
#             (service, region),
#             session.client(service, region_name=region) if region else session.client(service))
