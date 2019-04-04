from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.utils import get_non_provider_id


class LoadBalancers(Resources):

    def __init__(self, facade: AzureFacade):
        self.facade = facade

    async def fetch_all(self, credentials, **kwargs):
        self['load_balancers'] = {}
        for raw_load_balancer in await self.facade.loadbalancer.get_load_balancers():
            id, load_balancer = self._parse_load_balancer(raw_load_balancer)
            self['load_balancers'][id] = load_balancer

        self['load_balancers_count'] = len(self['load_balancers'])

    def _parse_load_balancer(self, load_balancer):
        load_balancer_dict = {}
        load_balancer_dict['id'] = get_non_provider_id(load_balancer.id)
        load_balancer_dict['name'] = load_balancer.name
        load_balancer_dict['forwarded_ports'] = self._get_forwarded_ports(
            load_balancer)

        return load_balancer_dict['id'], load_balancer_dict

    def _get_forwarded_ports(self, load_balancer):
        ports = []
        for rule in load_balancer.load_balancing_rules:
            ports.append(rule.frontend_port)

        return ports
