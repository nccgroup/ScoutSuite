import os

from ScoutSuite.core.console import print_exception

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.services import AzureServicesConfig


class AzureProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self,
                 subscription_ids=[], all_subscriptions=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None,
                 result_format='json',
                 **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'
        self.environment = 'default'

        self.programmatic_execution = kwargs['programmatic_execution']
        self.credentials = kwargs['credentials']

        if subscription_ids:
            self.subscription_ids = subscription_ids
        elif self.credentials.default_subscription_id:
            self.subscription_ids = [self.credentials.default_subscription_id]
        else:
            self.subscription_ids = []
        self.all_subscriptions = all_subscriptions

        try:
            self.account_id = self.credentials.get_tenant_id()
        except Exception as e:
            self.account_id = 'undefined'

        self.services = AzureServicesConfig(self.credentials,
                                            programmatic_execution=self.programmatic_execution,
                                            subscription_ids=self.subscription_ids,
                                            all_subscriptions=self.all_subscriptions)

        self.result_format = result_format

        super(AzureProvider, self).__init__(report_dir, timestamp,
                                            services, skipped_services, result_format)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        try:
            return 'azure-tenant-{}'.format(self.credentials.get_tenant_id())
        except Exception as e:
            print_exception('Unable to define report name: {}'.format(e))
            return 'azure'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        Tweak the Azure config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges

        self._match_arm_roles_and_principals()

        super(AzureProvider, self).preprocessing()

    def _match_arm_roles_and_principals(self):
        """
        Matches ARM roles to AAD service principals

        :return:
        """

        # Add role assignments
        if 'arm' in self.service_list and 'aad' in self.service_list:
            for subscription in self.services['arm']['subscriptions']:
                for assignment in self.services['arm']['subscriptions'][subscription]['role_assignments'].values():
                    role_id = assignment['role_definition_id'].split('/')[-1]
                    for group in self.services['aad']['groups']:
                        if group == assignment['principal_id']:
                            self.services['aad']['groups'][group]['roles'].append({'subscription_id': subscription,
                                                                                 'role_id': role_id})
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments']['groups'].append(group)
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments_count'] += 1
                    for user in self.services['aad']['users']:
                        if user == assignment['principal_id']:
                            self.services['aad']['users'][user]['roles'].append({'subscription_id': subscription,
                                                                                 'role_id': role_id})
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments']['users'].append(user)
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments_count'] += 1
                    for service_principal in self.services['aad']['service_principals']:
                        if service_principal == assignment['principal_id']:
                            self.services['aad']['service_principals'][service_principal]['roles'].append({'subscription_id': subscription,
                                                                                                           'role_id': role_id})
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments']['service_principals'].append(service_principal)
                            self.services['arm']['subscriptions'][subscription]['roles'][role_id]['assignments_count'] += 1
