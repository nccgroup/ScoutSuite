from ScoutSuite.providers.azure.resources.base import AzureCompositeResources


class Subscriptions(AzureCompositeResources):

    """This class represents a collection of Azure Resources that are grouped by subscription.
    Classes extending Subscriptions should implement the method _fetch_children() with a subscription ID as paramater.
    The children resources will be stored with the following structure {<subscriptions>: {<subscription_id>: {<child_name>: {<child_id>: <child_instance>}}}}.
    """

    async def fetch_all(self):
        """This method fetches all the Azure subscriptions that can be accessed with the given run configuration.
        It then fetches all the children defined in _children and groups them by subscription.
        """

        raw_subscriptions = await self.facade.get_subscriptions()

        if raw_subscriptions:
            self['subscriptions'] = {subscription.subscription_id: {}
                                     for subscription in raw_subscriptions}
        else:
            self['subscriptions'] = {}
        await self._fetch_children_of_all_resources(
            resources=self['subscriptions'],
            scopes={subscription_id: {'subscription_id': subscription_id} for subscription_id in self['subscriptions']})
        self._set_counts()

    def _set_counts(self):
        for _, child_name in self._children:
            self[child_name + '_count'] = sum([subscription[child_name + '_count']
                                               for subscription in self['subscriptions'].values()])
