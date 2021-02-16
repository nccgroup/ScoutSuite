from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_keys
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.core.console import print_exception


class LoadBalancers(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_load_balancers = await self.facade.elb.get_load_balancers(self.region, self.vpc)
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

    def _parse_load_balancer(self, raw_load_balancer):
        load_balancer = {'name': raw_load_balancer['LoadBalancerName']}
        get_keys(raw_load_balancer, load_balancer,
                 ['DNSName', 'CreatedTime', 'AvailabilityZones', 'Subnets', 'Scheme', 'attributes'])

        load_balancer['security_groups'] = []
        load_balancer['arn'] = 'arn:aws:elb:{}:{}:load-balancer/{}'.format(self.region,
                                                                           self.facade.owner_id,
                                                                           raw_load_balancer.get('LoadBalancerName'))
        for sg in raw_load_balancer['SecurityGroups']:
            load_balancer['security_groups'].append({'GroupId': sg})

        load_balancer['listeners'] = {}
        for l in raw_load_balancer['ListenerDescriptions']:
            listener = l['Listener']
            load_balancer['listeners'][l['Listener']
                                       ['LoadBalancerPort']] = listener

        load_balancer['instances'] = []
        for i in raw_load_balancer['Instances']:
            load_balancer['instances'].append(i['InstanceId'])

        if 'Tags' in raw_load_balancer and raw_load_balancer['Tags']:
            load_balancer['tags'] = {x['Key']: x['Value'] for x in raw_load_balancer['Tags']}

        return get_non_provider_id(load_balancer['name']), load_balancer
