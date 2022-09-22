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
                resources = self.get(endpoint)['items']
                kind = api_resource['kind'] 

                # Redact sensitive resources
                if kind in ['Secret']:
                    for i in range(len(resources)):
                        for key in resources[i]['data']:
                            resources[i]['data'][key] = 'REDACTED'

                data[kind] = data.get(kind, {})
                data[kind][version] = resources

        self.data = self.parse_data(data)
        return self.data