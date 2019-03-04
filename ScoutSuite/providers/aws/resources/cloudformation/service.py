from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade


class Stacks(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_stacks  = self.facade.cloudformation.get_stacks(self.scope['region'])
        for raw_stack in raw_stacks:
            name, stack = self._parse_stack(raw_stack)
            self[name] = stack

    def _parse_stack(self, raw_stack):
        raw_stack['id'] = raw_stack.pop('StackId')
        raw_stack['name'] = raw_stack.pop('StackName')
        raw_stack['drifted'] = raw_stack.pop('DriftInformation')['StackDriftStatus'] == 'DRIFTED'

        template = raw_stack.pop('template')
        raw_stack['deletion_policy'] = 'Delete'
        for group in template.keys():
            if 'DeletionPolicy' in template[group]:
                raw_stack['deletion_policy'] = template[group]['DeletionPolicy']
                break

        return raw_stack['name'], raw_stack



class CloudFormation(Regions):
    _children = [
        (Stack, 'stacks')
    ]

    def __init__(self):
        super(CloudFormation, self).__init__('cloudformation')
