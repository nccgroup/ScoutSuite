import json

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class LambdaFacade(AWSBaseFacade):
    async def get_functions(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('lambda', region, self.session, 'list_functions', 'Functions')
        except Exception as e:
            print_exception('Failed to get Lambda functions: {}'.format(e))
            return []

    async def get_access_policy(self, function_name, region):
        client = AWSFacadeUtils.get_client('lambda', self.session, region)
        try:
            policy = client.get_policy(FunctionName=function_name)
            if policy is not None and 'Policy' in policy:
                return json.loads(policy['Policy'])
        except Exception:
            # Policy not found for this function
            return None
