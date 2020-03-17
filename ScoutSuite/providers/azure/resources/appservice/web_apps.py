from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class WebApplication(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(WebApplication, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_web_app in await self.facade.appservice.get_web_apps(self.subscription_id):
            id, web_app = self._parse_web_app(raw_web_app)
            self[id] = web_app

    def _parse_web_app(self, raw_web_app):

        web_app_dict = {}
        web_app_dict['id'] = get_non_provider_id(raw_web_app.id)
        web_app_dict['name'] = raw_web_app.name
        web_app_dict['kind'] = raw_web_app.kind
        web_app_dict['location'] = raw_web_app.location
        web_app_dict['type'] = raw_web_app.type
        web_app_dict['tags'] = raw_web_app.tags
        web_app_dict['state'] = raw_web_app.state
        web_app_dict['host_names'] = raw_web_app.host_names
        web_app_dict['repository_site_name'] = raw_web_app.repository_site_name
        web_app_dict['usage_state'] = raw_web_app.usage_state
        web_app_dict['enabled'] = raw_web_app.enabled
        web_app_dict['https_only'] = raw_web_app.https_only
        web_app_dict['enabled_host_names'] = raw_web_app.enabled_host_names
        web_app_dict['availability_state'] = raw_web_app.availability_state
        web_app_dict['host_name_ssl_states'] = raw_web_app.host_name_ssl_states
        web_app_dict['server_farm_id'] = raw_web_app.server_farm_id
        web_app_dict['reserved'] = raw_web_app.reserved
        web_app_dict['is_xenon'] = raw_web_app.is_xenon
        web_app_dict['hyper_v'] = raw_web_app.hyper_v
        web_app_dict['last_modified_time_utc'] = raw_web_app.last_modified_time_utc
        web_app_dict['site_config'] = raw_web_app.site_config
        web_app_dict['traffic_manager_host_names'] = raw_web_app.traffic_manager_host_names
        web_app_dict['scm_site_also_stopped'] = raw_web_app.scm_site_also_stopped
        web_app_dict['target_swap_slot'] = raw_web_app.target_swap_slot
        web_app_dict['hosting_environment_profile'] = raw_web_app.hosting_environment_profile
        web_app_dict['client_affinity_enabled'] = raw_web_app.client_affinity_enabled
        web_app_dict['client_cert_enabled'] = raw_web_app.client_cert_enabled
        web_app_dict['client_cert_exclusion_paths'] = raw_web_app.client_cert_exclusion_paths
        web_app_dict['host_names_disabled'] = raw_web_app.host_names_disabled
        web_app_dict['outbound_ip_addresses'] = raw_web_app.outbound_ip_addresses
        web_app_dict['possible_outbound_ip_addresses'] = raw_web_app.possible_outbound_ip_addresses
        web_app_dict['container_size'] = raw_web_app.container_size
        web_app_dict['daily_memory_time_quota'] = raw_web_app.daily_memory_time_quota
        web_app_dict['suspended_till'] = raw_web_app.suspended_till
        web_app_dict['max_number_of_workers'] = raw_web_app.max_number_of_workers
        web_app_dict['cloning_info'] = raw_web_app.cloning_info
        web_app_dict['resource_group'] = raw_web_app.resource_group
        web_app_dict['is_default_container'] = raw_web_app.is_default_container
        web_app_dict['default_host_name'] = raw_web_app.default_host_name
        web_app_dict['slot_swap_status'] = raw_web_app.slot_swap_status
        web_app_dict['redundancy_mode'] = raw_web_app.redundancy_mode
        web_app_dict['in_progress_operation_id'] = raw_web_app.in_progress_operation_id
        web_app_dict['identity'] = raw_web_app.identity
        web_app_dict['additional_properties'] = raw_web_app.additional_properties

        if raw_web_app.config is not None:
            web_app_dict['minimum_tls_version_supported'] = raw_web_app.config.min_tls_version
            web_app_dict['http_2_enabled'] = raw_web_app.config.http20_enabled

            # TODO handle this
            if raw_web_app.config.net_framework_version:
                web_app_dict['programming_language'] = 'dotnet'
                web_app_dict['programming_language_version'] = raw_web_app.config.net_framework_version
            elif raw_web_app.config.php_version:
                web_app_dict['programming_language'] = 'php'
                web_app_dict['programming_language_version'] = raw_web_app.config.php_version
            elif raw_web_app.config.python_version:
                web_app_dict['programming_language'] = 'python'
                web_app_dict['programming_language_version'] = raw_web_app.config.python_version
            elif raw_web_app.config.node_version:
                web_app_dict['programming_language'] = 'node'
                web_app_dict['programming_language_version'] = raw_web_app.config.node_version
            elif raw_web_app.config.java_version:
                web_app_dict['programming_language'] = 'java'
                web_app_dict['programming_language_version'] = raw_web_app.config.java_version
            else:
                web_app_dict['programming_language'] = None
                web_app_dict['programming_language_version'] = None

            # TODO - write rules for this values
            # web_app_dict[''] = raw_web_app.config.cors
            # web_app_dict[''] = raw_web_app.config.http_logging_enabled
            # web_app_dict[''] = raw_web_app.config.ftps_state
            # also look at network configuration / IP security restrictions
        else:
            web_app_dict['minimum_tls_version_supported'] = None
            web_app_dict['http_2_enabled'] = None
            web_app_dict['programming_language'] = None
            web_app_dict['programming_language_version'] = None

        if raw_web_app.auth_settings is not None:
            web_app_dict['authentication_enabled'] = raw_web_app.auth_settings.enabled
        else:
            web_app_dict['authentication_enabled'] = None

        return web_app_dict['id'], web_app_dict
