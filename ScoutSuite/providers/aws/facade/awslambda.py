import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade:
    def get_functions(self, region):
        return AWSFacadeUtils.get_all_pages('lambda', region, 'list_functions', 'Functions')
