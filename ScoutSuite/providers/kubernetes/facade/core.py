from ScoutSuite.core.console import print_error
from ScoutSuite.providers.kubernetes.facade.base import KubernetesBaseFacade


class CoreFacade(KubernetesBaseFacade):
    def __init__(self, credentials):
        super().__init__(credentials)

    def get_resource_definitions(self) -> dict:
        if self.resource_definitions != None:
            return self.resource_definitions

        self.resource_definitions = {}
        for version in self.get('/api')['versions']:
            self.resource_definitions[version] = self.get(f'/api/{version}')['resources']

        return self.resource_definitions

    def get_resources(self) -> dict:
        if self.data != None: return self.data

        data = {}
        core_resource_definitions = self.get_resource_definitions()

        for version in core_resource_definitions:
            core_resources = core_resource_definitions[version]
            for api_resource in core_resources:
                if 'list' not in api_resource['verbs']: continue
                endpoint = f'''/api/{version}/{api_resource['name']}'''
                
                resources = self.get(endpoint)
                if not resources:
                    continue
                
                resource_items = resources['items']
                kind = api_resource['kind']

                # Redact sensitive resources
                if kind in ['Secret']:
                    for i in range(len(resource_items)):
                        # Do not naively assume all secrets have `data`
                        secret_data = resource_items[i].get('data')
                        if not secret_data: continue

                        # Do not assume `data` is a dictionary either
                        if type(secret_data) == dict:
                            for key in secret_data:
                                resource_items[i]['data'][key] = 'REDACTED'
                        elif type(secret_data) == str:
                            resource_items[i]['data'] = 'REDACTED'
                        elif type(secret_data) == list:
                            for j in range(len(secret_data)):
                                resource_items[i]['data'][j] = 'REDACTED'

                data[kind] = data.get(kind, {})
                data[kind][version] = resource_items

        self.data = self.parse_data(data)
        return self.data