from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Listeners(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, load_balancer_arn: str):
        super().__init__(facade)
        self.region = region
        self.load_balancer_arn = load_balancer_arn

    async def fetch_all(self):
        listeners = await self.facade.elbv2.get_listeners(self.region, self.load_balancer_arn)
        parsing_error_counter = 0
        for raw_listener in listeners:
            try:
                id, listener = self._parse_listener(raw_listener)
                self[id] = listener
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_listener(self, raw_listener):
            raw_listener.pop('ListenerArn')
            raw_listener.pop('LoadBalancerArn')
            port = raw_listener.pop('Port')
            return port, raw_listener
