import json

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently


class CloudFormation:
    async def get_stacks(self, region: str):
        stacks = await AWSFacadeUtils.get_all_pages('cloudformation', region, 'list_stacks', 'StackSummaries')
        stacks = [stack for stack in stacks if not CloudFormation._is_stack_deleted(stack)]
        client = AWSFacadeUtils.get_client('cloudformation', region)
        for stack in stacks:
            stack_name = stack['StackName']

            stack_description = await run_concurrently(
                        lambda: client.describe_stacks(StackName=stack_name)['Stacks'][0]
            )
            stack.update(stack_description)
            stack['template'] = await run_concurrently(
                        lambda: client.get_template(StackName=stack_name)['TemplateBody']
            )
            stack_policy = await run_concurrently(
                        lambda: client.get_stack_policy(StackName=stack_name)
            )
            if 'StackPolicyBody' in stack_policy:
                 stack['policy'] = json.loads(stack_policy['StackPolicyBody'])

        return stacks

    @staticmethod
    def _is_stack_deleted(stack):
        return stack.get('StackStatus', None) == 'DELETE_COMPLETE'