from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.azure.facade.aad import AADFacade
from ScoutSuite.providers.azure.facade.arm import ARMFacade
from ScoutSuite.providers.azure.facade.keyvault import KeyVaultFacade
from ScoutSuite.providers.azure.facade.network import NetworkFacade
from ScoutSuite.providers.azure.facade.securitycenter import SecurityCenterFacade
from ScoutSuite.providers.azure.facade.sqldatabase import SQLDatabaseFacade
from ScoutSuite.providers.azure.facade.storageaccounts import StorageAccountsFacade
from ScoutSuite.providers.azure.facade.virtualmachines import VirtualMachineFacade
from ScoutSuite.providers.azure.facade.appservice import AppServiceFacade

from azure.mgmt.resource import SubscriptionClient

from ScoutSuite.core.console import print_info, print_exception

# Try to import proprietary services
try:
    from ScoutSuite.providers.azure.facade.appgateway_private import AppGatewayFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.facade.loadbalancer_private import LoadBalancerFacade
except ImportError:
    pass
try:
    from ScoutSuite.providers.azure.facade.rediscache_private import RedisCacheFacade
except ImportError:
    pass


class AzureFacade:
    def __init__(self,
                 credentials: AzureCredentials,
                 subscription_ids=[], all_subscriptions=False,
                 programmatic_execution=False):

        self.credentials = credentials
        self.programmatic_execution = programmatic_execution

        self.subscription_list = []
        self.subscription_ids = subscription_ids
        self.all_subscriptions = all_subscriptions

        self.aad = AADFacade(credentials)
        self.arm = ARMFacade(credentials)
        self.keyvault = KeyVaultFacade(credentials)
        self.virtualmachines = VirtualMachineFacade(credentials)
        self.network = NetworkFacade(credentials)
        self.securitycenter = SecurityCenterFacade(credentials)
        self.sqldatabase = SQLDatabaseFacade(credentials)
        self.storageaccounts = StorageAccountsFacade(credentials)
        self.appservice = AppServiceFacade(credentials)

        # Instantiate facades for proprietary services
        try:
            self.appgateway = AppGatewayFacade(credentials)
        except NameError:
            pass
        try:
            self.loadbalancer = LoadBalancerFacade(credentials)
        except NameError:
            pass
        try:
            self.rediscache = RedisCacheFacade(credentials)
        except NameError:
            pass

        self._set_subscriptions()

    async def get_subscriptions(self):
        if self.subscription_list:
            return self.subscription_list
        else:
            self._set_subscriptions()

    def _set_subscriptions(self):

        # Create the client
        subscription_client = SubscriptionClient(self.credentials.arm_credentials)
        # Get all the accessible subscriptions
        accessible_subscriptions_list = list(subscription_client.subscriptions.list())

        if not accessible_subscriptions_list:
            print_exception('The provided credentials do not have access to any subscriptions')
            self.subscription_list = []
            return

        # Final list, start empty
        subscriptions_list = []

        # No subscription provided, infer
        if not (self.subscription_ids or self.all_subscriptions):
            try:
                # Tries to read the subscription list
                print_info('No subscription set, inferring ID')
                s = next(subscription_client.subscriptions.list())
            except StopIteration:
                print_info('Unable to infer a subscription')
                # If the user cannot read subscription list, ask Subscription ID:
                if not self.programmatic_execution:
                    s = input('Subscription ID: ')
                else:
                    print_exception('Unable to infer a Subscription ID')
                    raise
            finally:
                print_info('Running against the "{}" subscription'.format(s.subscription_id))
                subscriptions_list.append(s)

        # A specific set of subscriptions
        elif self.subscription_ids:
            # Only include accessible subscriptions
            subscriptions_list = [s for s in accessible_subscriptions_list if
                                  s.subscription_id in self.subscription_ids]
            # Verbose skip
            for s in self.subscription_ids:
                if not any(subs.subscription_id == s for subs in accessible_subscriptions_list):
                    print_info('Skipping subscription "{}": this subscription does not exist or '
                               'is not accessible with the provided credentials'.format(s))
            print_info('Running against {} subscription(s)'.format(len(subscriptions_list)))

        # All subscriptions
        elif self.all_subscriptions:
            subscriptions_list = accessible_subscriptions_list
            print_info('Running against {} subscription(s)'.format(len(subscriptions_list)))

        # Other == error
        else:
            print_exception('Unknown Azure subscription option')
            self.subscription_list = []
            raise

        if subscriptions_list:
            self.subscription_list = subscriptions_list
        else:
            print_exception('No subscriptions to scan')
            self.subscription_list = []
            raise
