from ScoutSuite.providers.aws.resources.resources import AWSResources
from ScoutSuite.providers.aws.utils import get_keys
from ScoutSuite.providers.utils import get_non_provider_id


class LoadBalancers(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_load_balancers = await self.facade.elb.get_load_balancers(self.scope['region'], self.scope['vpc'])
        # TODO: parse is async, parallelize the following loop:
        for raw_load_balancer in raw_load_balancers:
            id, load_balancer = await self._parse_load_balancer(raw_load_balancer)
            self[id] = load_balancer

    async def _parse_load_balancer(self, raw_load_balancer):
        load_balancer = {'name': raw_load_balancer.pop('LoadBalancerName')}
        get_keys(raw_load_balancer, load_balancer, ['DNSName', 'CreatedTime', 'AvailabilityZones', 'Subnets', 'Scheme'])

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

        load_balancer['attributes'] =\
            await self.facade.elb.get_load_balancer_attributes(self.scope['region'], load_balancer['name'])

        return get_non_provider_id(load_balancer['name']), load_balancer
