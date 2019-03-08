from ScoutSuite.providers.utils import run_concurrently

class GCPFacadeUtils:
    @staticmethod
    async def get_all(resource_key, request, resources_group):
        resources = []
        while request is not None:
            response = await run_concurrently(request.execute)
            resources.extend(response.get(resource_key, []))
            request = await run_concurrently(
                        lambda: resources_group.list_next(previous_request=request, previous_response=response)
            )
        return resources