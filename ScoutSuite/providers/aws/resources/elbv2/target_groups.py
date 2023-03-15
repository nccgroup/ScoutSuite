from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class TargetGroups(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, load_balancer_arn: str):
        super().__init__(facade)
        self.region = region
        self.load_balancer_arn = load_balancer_arn

    async def fetch_all(self):
        target_groups = await self.facade.elbv2.get_target_groups(self.region, self.load_balancer_arn)
        for raw_target_group in target_groups:
            arn, target_group = self._parse_target_groups(raw_target_group)
            self[arn] = target_group

    def _parse_target_groups(self, raw_target_group):
            raw_target_group.pop('LoadBalancerArns')
            arn = raw_target_group.pop('TargetGroupArn')
            return arn, raw_target_group
