import asyncio

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.utils import ec2_classic
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently, map_concurrently
from ScoutSuite.providers.utils import get_non_provider_id


class ELBFacade(AWSBaseFacade):
    regional_load_balancers_cache_locks = {}
    load_balancers_cache = {}
    policies_cache = set()

    async def get_load_balancers(self, region: str, vpc: str):
        try:
            await self.cache_load_balancers(region)
            return [load_balancer for load_balancer in self.load_balancers_cache[region] if load_balancer['VpcId'] == vpc]
        except Exception as e:
            print_exception(f'Failed to get ELB load balancers: {e}')
            return []

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

            await get_and_set_concurrently(
                [self._get_and_set_load_balancer_tags], self.load_balancers_cache[region], region=region)

    async def _get_and_set_load_balancer_attributes(self, load_balancer: {}, region: str):
        elb_client = AWSFacadeUtils.get_client('elb', self.session, region)
        try:
            load_balancer['attributes'] = await run_concurrently(
                lambda: elb_client.describe_load_balancer_attributes(
                    LoadBalancerName=load_balancer['LoadBalancerName'])['LoadBalancerAttributes']
            )
        except Exception as e:
            print_exception(f'Failed to describe ELB load balancer attributes: {e}')

    async def _get_and_set_load_balancer_tags(self, load_balancer: {}, region: str):
        elb_client = AWSFacadeUtils.get_client('elb', self.session, region)
        try:
            load_balancer['Tags'] = await run_concurrently(
                lambda: elb_client.describe_tags(
                    LoadBalancerNames=[load_balancer['LoadBalancerName']])['TagDescriptions'][0]['Tags']
            )
        except Exception as e:
            print_exception(f'Failed to describe ELB load balancer tags: {e}')

    async def get_policies(self, region: str):
        try:
            await self.cache_load_balancers(region)
            for load_balancer in self.load_balancers_cache[region]:
                load_balancer['policy_names'] = []
                for listener_description in load_balancer['ListenerDescriptions']:
                    for policy_name in listener_description['PolicyNames']:
                        policy_id = get_non_provider_id(policy_name)
                        if policy_id not in self.policies_cache:
                            load_balancer['policy_names'].append(policy_name)
                            self.policies_cache.add(policy_id)

            policies = await map_concurrently(self._get_policies, self.load_balancers_cache[region], region=region)
            # Because _get_policies returns a list, policies has to be flatten:
            return [policy for nested_policy in policies for policy in nested_policy]
        except Exception as e:
            print_exception(f'Failed to describe ELB policies: {e}')
            return []

    async def _get_policies(self, load_balancer: dict, region: str):
            if len(load_balancer['policy_names']) == 0:
                return []

            elb_client = AWSFacadeUtils.get_client('elb', self.session, region)
            try:
                return await run_concurrently(lambda: elb_client.describe_load_balancer_policies(
                    LoadBalancerName=load_balancer['LoadBalancerName'],
                    PolicyNames=load_balancer['policy_names'])['PolicyDescriptions']
                )
            except Exception as e:
                print_exception(f'Failed to retrieve load balancer policies: {e}')
                return []
