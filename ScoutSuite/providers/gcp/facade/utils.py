from ScoutSuite.providers.utils import run_concurrently

class GCPFacadeUtils:
    @staticmethod
    def _get_all(resources, resource_key: str, request, resources_group):
        while request is not None:
            response = request.execute()
            resources.extend(response.get(resource_key, []))
            request = resources_group.list_next(previous_request=request, previous_response=response)

    @staticmethod
    async def get_all(resource_key: str, request, resources_group):
        resources = []
        await run_concurrently(
            lambda: GCPFacadeUtils._get_all(resources, resource_key, request, resources_group)
        )
        return resources
