import asyncio

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.utils import ec2_classic
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently


class ELBFacade(AWSBaseFacade):
    regional_load_balancers_cache_locks = {}
    load_balancers_cache = {}

    async def get_load_balancers(self, region: str, vpc: str):
        await self.cache_load_balancers(region)
        return [load_balancer for load_balancer in self.load_balancers_cache[region] if load_balancer['VpcId'] == vpc]

    async def cache_load_balancers(self, region):
        async with self.regional_load_balancers_cache_locks.setdefault(region, asyncio.Lock()):
            if region in self.load_balancers_cache:
                return

            self.load_balancers_cache[region] = \
                await AWSFacadeUtils.get_all_pages('elb', region, self.session,
                                                   'describe_load_balancers', 'LoadBalancerDescriptions')

            for load_balancer in self.load_balancers_cache[region]:
                load_balancer['VpcId'] = \
                    load_balancer['VPCId'] if 'VPCId' in load_balancer and load_balancer['VPCId'] else ec2_classic

            await get_and_set_concurrently(
                [self._get_and_set_load_balancer_attributes], self.load_balancers_cache[region], region=region)

    async def _get_and_set_load_balancer_attributes(self, load_balancer: {}, region: str):
        elb_client = AWSFacadeUtils.get_client('elb', self.session, region)
        try:
            load_balancer['attributes'] = await run_concurrently(
                lambda: elb_client.describe_load_balancer_attributes(
                    LoadBalancerName=load_balancer['LoadBalancerName'])['LoadBalancerAttributes']
            )
        except Exception as e:
            print_exception('Failed to describe ELB load balancer attributes: {}'.format(e))
