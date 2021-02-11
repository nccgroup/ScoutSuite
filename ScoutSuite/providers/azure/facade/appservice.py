from azure.mgmt.web import WebSiteManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.utils import get_user_agent


class AppServiceFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = WebSiteManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id, user_agent=get_user_agent())
        return client

    async def get_web_apps(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            web_apps = await run_concurrently(
                lambda: list(client.web_apps.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve web apps: {e}')
            return []
        else:
            await get_and_set_concurrently([self._get_and_set_web_app_configuration], web_apps, api_client=client)
            await get_and_set_concurrently([self._get_and_set_web_app_auth_settings], web_apps, api_client=client)
            return web_apps

    async def _get_and_set_web_app_configuration(self, web_app, api_client):
        resource_group_name = get_resource_group_name(web_app.id)
        try:
            web_app_config = await run_concurrently(
                lambda: api_client.web_apps.get_configuration(resource_group_name, web_app.name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve web app configuration: {e}')
            setattr(web_app, 'config', None)
        else:
            setattr(web_app, 'config', web_app_config)

    async def _get_and_set_web_app_auth_settings(self, web_app, api_client):
        resource_group_name = get_resource_group_name(web_app.id)
        try:
            web_app_auth_settings = await run_concurrently(
                lambda: api_client.web_apps.get_auth_settings(resource_group_name=resource_group_name,
                                                              name=web_app.name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve web app auth settings: {e}')
            setattr(web_app, 'auth_settings', None)
        else:
            setattr(web_app, 'auth_settings', web_app_auth_settings)
