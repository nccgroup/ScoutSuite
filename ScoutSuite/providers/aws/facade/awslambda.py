import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade:
    def get_functions(self, region):
        aws_lambda = boto3.client('lambda', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda: aws_lambda.list_functions(),
            lambda response: response['Functions']
        )
