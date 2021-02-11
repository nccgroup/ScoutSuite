from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .listeners import Listeners
from ScoutSuite.core.console import print_exception


class LoadBalancers(AWSCompositeResources):
    _children = [
        (Listeners, 'listeners')
    ]

    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_load_balancers = await self.facade.elbv2.get_load_balancers(self.region, self.vpc)
        parsing_error_counter = 0
        for raw_load_balancer in raw_load_balancers:
            try:
                id, load_balancer = self._parse_load_balancer(raw_load_balancer)
                self[id] = load_balancer
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={load_balancer_id: {'region': self.region, 'load_balancer_arn': load_balancer['arn']}
                    for (load_balancer_id, load_balancer) in self.items()}
        )

        # After loading the listener information, map the protocols used in a new field for easier usage in rules
        for lb_id in self.keys():
            if lb_id is not None and len(self[lb_id]['listeners']) > 0:
                protocols = [x['Protocol'] for x in list(self[lb_id]['listeners'].values())]
                self[lb_id]['listener_protocols'] = protocols

    def _parse_load_balancer(self, load_balancer):
        load_balancer['arn'] = load_balancer.pop('LoadBalancerArn')
        load_balancer['name'] = load_balancer.pop('LoadBalancerName')
        load_balancer['security_groups'] = []
        load_balancer['listener_protocols'] = []
        load_balancer['isNetwork'] = load_balancer["Type"] == "network"

        if 'SecurityGroups' in load_balancer:
            for sg in load_balancer['SecurityGroups']:
                load_balancer['security_groups'].append({'GroupId': sg})
            load_balancer.pop('SecurityGroups')

        if 'Tags' in load_balancer and load_balancer['Tags']:
            load_balancer['tags'] = {x['Key']: x['Value'] for x in load_balancer['Tags']}
            load_balancer.pop('Tags')

        return get_non_provider_id(load_balancer['name']), load_balancer
