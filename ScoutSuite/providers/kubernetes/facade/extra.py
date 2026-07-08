from ScoutSuite.core.console import print_error
from ScoutSuite.providers.kubernetes.facade.base import KubernetesBaseFacade


class ExtraFacade(KubernetesBaseFacade):
    def __init__(self, credentials):
        super().__init__(credentials)
        self.api_groups = None

    def get_resource_definitions(self) -> dict:
        if self.resource_definitions != None:
            return self.resource_definitions

        self.resource_definitions = self.get('/apis')

        return self.resource_definitions

    def get_resources(self) -> dict:
        if self.data != None: return self.data

        data = {}

        extra_resources = self.get_resource_definitions()
        for group in extra_resources['groups']:
            for version in group['versions']:
                endpoint = f'''/apis/{version['groupVersion']}'''

                api_resources = self.get(endpoint)
                if not api_resources:
                    continue

                for api_resource in api_resources['resources']:
                    if 'list' not in api_resource['verbs']: continue
                    endpoint = f'''/apis/{version['groupVersion']}/{api_resource['name']}'''

                    api_resources = self.get(endpoint)
                    if not api_resources:
                        continue

                    resources = self.get(endpoint)['items']
                    key = api_resource['kind']
                    data[key] = data.get(key, {})
                    data[key][version['groupVersion']] = resources

        self.data = self.parse_data(data)
        return self.data