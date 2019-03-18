from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.utils import get_keys
from ScoutSuite.providers.utils import get_non_provider_id


class LoadBalancers(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_load_balancers = await self.facade.elb.get_load_balancers(self.scope['region'], self.scope['vpc'])
        for raw_load_balancer in raw_load_balancers:
            id, load_balancer = self._parse_load_balancer(raw_load_balancer)
            self[id] = load_balancer

    def _parse_load_balancer(self, raw_load_balancer):
        load_balancer = {'name': raw_load_balancer.pop('LoadBalancerName')}
        get_keys(raw_load_balancer, load_balancer,
                 ['DNSName', 'CreatedTime', 'AvailabilityZones', 'Subnets', 'Scheme', 'attributes'])

        load_balancer['security_groups'] = []
        for sg in raw_load_balancer['SecurityGroups']:
            load_balancer['security_groups'].append({'GroupId': sg})

        load_balancer['listeners'] = {}
        for l in raw_load_balancer['ListenerDescriptions']:
            listener = l['Listener']
            load_balancer['listeners'][l['Listener']['LoadBalancerPort']] = listener

        load_balancer['instances'] = []
        for i in raw_load_balancer['Instances']:
            load_balancer['instances'].append(i['InstanceId'])

        return get_non_provider_id(load_balancer['name']), load_balancer
