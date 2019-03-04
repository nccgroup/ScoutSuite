import json

from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class CloudFormation:
    def get_stacks(self, region: str):
        stacks = AWSFacadeUtils.get_all_pages('cloudformation', region, 'list_stacks', 'StackSummaries')

        client = AWSFacadeUtils.get_client('cloudformation', region)
        for stack in stacks:
            stack_name = stack['StackName']
            stack_description = client.describe_stacks(StackName=stack_name)['Stacks'][0]
            stack.update(stack_description)
            stack['template'] = client.get_template(StackName=stack_name)['TemplateBody']
            stack_policy = client.get_stack_policy(StackName=stack_name)
            if 'StackPolicyBody' in stack_policy:
                 stack['policy'] = json.loads(stack_policy['StackPolicyBody'])

        return stacks
