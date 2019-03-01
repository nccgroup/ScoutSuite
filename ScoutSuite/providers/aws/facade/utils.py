from typing import Callable
import boto3

class AWSFacadeUtils:
    _clients = {}
    
    @staticmethod
    def get_all_pages(service, region, paginator_name: str, response_key: str, **paginator_args):
        pages = AWSFacadeUtils.get_client(service, region) \
                              .get_paginator(paginator_name) \
                              .paginate(**paginator_args)
                                   
        return AWSFacadeUtils._get_from_all_pages(pages, response_key)

    @staticmethod
    def _get_from_all_pages(pages: [], key:str):
        resources = []
        for page in pages:
            resources.extend(page[key])

        return resources

    @staticmethod
    def get_client(service: str, region: str):
        return AWSFacadeUtils._clients.setdefault((service, region), boto3.client(service, region_name=region))