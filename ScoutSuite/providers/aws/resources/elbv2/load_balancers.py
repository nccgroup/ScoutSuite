import asyncio

from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .listeners import Listeners


class LoadBalancers(AWSCompositeResources):
    _children = [
        (Listeners, 'listeners')
    ]

    async def fetch_all(self, **kwargs):
        raw_loads_balancers = await self.facade.elbv2.get_load_balancers(self.scope['region'], self.scope['vpc'])
        await asyncio.wait({asyncio.ensure_future(self._fetch_one(raw_load_balancer)) for raw_load_balancer in raw_loads_balancers})
            
    async def _fetch_one(self, raw_load_balancer):
        id, load_balancer = await self._parse_load_balancer(raw_load_balancer)
        self[id] = load_balancer
        await self._fetch_children(parent=load_balancer, scope={'region': self.scope['region'], 'load_balancer_arn': load_balancer['arn']})


    async def _parse_load_balancer(self, load_balancer):
        load_balancer['arn'] = load_balancer.pop('LoadBalancerArn')
        load_balancer['name'] = load_balancer.pop('LoadBalancerName')
        load_balancer['security_groups'] = []

        if 'SecurityGroups' in load_balancer:
            for sg in load_balancer['SecurityGroups']:
                load_balancer['security_groups'].append({'GroupId': sg})
            load_balancer.pop('SecurityGroups')

        load_balancer['attributes'] =\
            await self.facade.elbv2.get_load_balancer_attributes(self.scope['region'], load_balancer['arn'])

        return get_non_provider_id(load_balancer['name']), load_balancer
