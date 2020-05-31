import json

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import get_and_set_concurrently
from ScoutSuite.providers.utils import run_concurrently


class CloudFormation(AWSBaseFacade):

    async def get_stacks(self, region: str):
        try:
            stacks = await AWSFacadeUtils.get_all_pages(
                'cloudformation', region, self.session, 'list_stacks', 'StackSummaries')
        except Exception as e:
            print_exception('Failed to get CloudFormation stack: {}'.format(e))
            stacks = []
        else:
            stacks = [stack for stack in stacks if not CloudFormation._is_stack_deleted(stack)]
            await get_and_set_concurrently(
                [self._get_and_set_description, self._get_and_set_template, self._get_and_set_policy],
                stacks, region=region)
        finally:
            return stacks

    async def _get_and_set_description(self, stack: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudformation', self.session, region)
        try:
            stack_description = await run_concurrently(
                lambda: client.describe_stacks(StackName=stack['StackName'])['Stacks'][0])
        except Exception as e:
            print_exception('Failed to describe CloudFormation stack: {}'.format(e))
        else:
            stack.update(stack_description)

    async def _get_and_set_template(self, stack: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudformation', self.session, region)
        try:
            stack['template'] = await run_concurrently(
                lambda: client.get_template(StackName=stack['StackName'])['TemplateBody'])
        except Exception as e:
            print_exception('Failed to get CloudFormation template: {}'.format(e))
            stack['template'] = None

    async def _get_and_set_policy(self, stack: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudformation', self.session, region)
        try:
            stack_policy = await run_concurrently(
                lambda: client.get_stack_policy(StackName=stack['StackName']))
        except Exception as e:
            print_exception('Failed to get CloudFormation stack policy: {}'.format(e))
        else:
            if 'StackPolicyBody' in stack_policy:
                stack['policy'] = json.loads(stack_policy['StackPolicyBody'])

    @staticmethod
    def _is_stack_deleted(stack):
        return stack.get('StackStatus', None) == 'DELETE_COMPLETE'
