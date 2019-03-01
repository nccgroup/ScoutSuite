import boto3
import base64
import itertools

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade:
    def get_functions(self, region):
        aws_lambda = boto3.client('lambda', region_name=region)
        return AWSFacadeUtils.get_all_pages(
            lambda marker: aws_lambda.list_functions(Marker=marker),
            lambda response: response['Functions'],
            'Marker'
        )
