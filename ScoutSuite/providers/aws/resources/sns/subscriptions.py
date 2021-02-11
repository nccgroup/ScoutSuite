from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Subscriptions(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, topic_name: str):
        super().__init__(facade)
        self.region = region
        self.topic_name = topic_name

    async def fetch_all(self):
        raw_subscriptions = await self.facade.sns.get_subscriptions(self.region, self.topic_name)
        self['protocol'] = {}
        self['subscriptions_count'] = 0
        parsing_error_counter = 0
        for raw_subscription in raw_subscriptions:
            try:
                protocol, subscription = self._parse_subscription(raw_subscription)
                if protocol in self['protocol']:
                    self['protocol'][protocol].append(subscription)
                else:
                    self['protocol'][protocol] = [subscription]
                self['subscriptions_count'] += 1
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_subscription(self, raw_subscription):
        protocol = raw_subscription.pop('Protocol')
        return protocol, raw_subscription
