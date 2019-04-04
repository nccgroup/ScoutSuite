from ScoutSuite.providers.aws.resources.base import AWSResources


class Subscriptions(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_subscriptions = await self.facade.sns.get_subscriptions(self.scope['region'], self.scope['topic_name'])
        self['protocol'] = {}
        self['subscriptions_count'] = 0
        for raw_subscription in raw_subscriptions:
            protocol, subscription = self._parse_subscription(raw_subscription)
            if protocol in self['protocol']:
                self['protocol'][protocol].append(subscription)
            else:
                self['protocol'][protocol] = [subscription]
            self['subscriptions_count'] += 1

    def _parse_subscription(self, raw_subscription):
        protocol = raw_subscription.pop('Protocol')
        return protocol, raw_subscription
