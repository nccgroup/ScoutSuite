from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class StackSets(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_stacksets = await self.facade.cloudformation.get_stacksets(self.region)
        for raw_stackset in raw_stacksets:
            name, stack = self._parse_stackset(raw_stackset)
            self[name] = stack

    def _parse_stackset(self, raw_stackset):
        stackset = {}
        stackset['id'] = raw_stackset.get('StackSetId')
        stackset['name'] = raw_stackset.get('StackSetName')
        if 'Description' in raw_stackset:
            stackset['description'] = raw_stackset.get('Description')
        stackset['status'] = raw_stackset.get('Status')
        stackset['permission_model'] = raw_stackset.get('PermissionModel')
        stackset['drift_status'] = raw_stackset.get('DriftStatus')
        if 'LastDriftCheckTimestamp' in raw_stackset:
            stackset['last_drift_check_timestamp'] = raw_stackset.get('LastDriftCheckTimestamp')
        
        return stackset['name'], stackset
