from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent

from googleapiclient import http



class GCPFacadeUtils:
    @staticmethod
    async def _get_all(resources, resource_key: str, request, resources_group):
        while request is not None:
            response = request.execute()
            resources.extend(response.get(resource_key, []))
            request = await run_concurrently(
                lambda: resources_group.list_next(previous_request=request, previous_response=response)
            )

    @staticmethod
    async def get_all(resource_key: str, request, resources_group):
        # force set custom user agent
        http.set_user_agent(request.http, get_user_agent())
        request.headers['user-agent'] = get_user_agent()

        resources = []
        await GCPFacadeUtils._get_all(resources, resource_key, request, resources_group)
        return resources
