from json import dumps, loads
from yaml import safe_dump

from google.auth.credentials import Credentials as GCPCredentials
from kubernetes.client.exceptions import ApiException

from ScoutSuite.core.console import print_error, print_info
from ScoutSuite.providers.aws.authentication_strategy import AWSCredentials
from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.kubernetes.authentication_strategy import ClusterProvider, KubernetesCredentials
from ScoutSuite.providers.kubernetes.utils import format_api_version, format_resource_id, format_resource_kind, format_resource_name


from ScoutSuite import __version__


class KubernetesBaseFacade:
    def continue_upon_exception(function):
        def continue_upon_exception_callback(self, **kwargs):
            try:
                return function(self, **kwargs)
            except ApiException as api_exception:
                print(api_exception)
                print_error(f'[{api_exception.__class__.__name__}] {function.__module__}.{function.__name__}: {api_exception.reason}')
                return None
            except Exception as exception:
                print(exception)
                print_error(f'[{exception.__class__.__name__}] {function.__module__}.{function.__name__}: {exception}')
                return None
        return continue_upon_exception_callback

    def __init__(self, credentials: KubernetesCredentials) -> None:
        self.resource_definitions = None
        self.data = None
        self.cluster_provider = None
        self.api_client = credentials.api_client
        self.api_client.user_agent = f'Scout Suite {__version__}'

        if isinstance(credentials, AzureCredentials):
            self.cluster_provider = ClusterProvider.AKS.value
        elif isinstance(credentials, AWSCredentials):
            self.cluster_provider = ClusterProvider.EKS.value
        elif isinstance(credentials, GCPCredentials):
            self.cluster_provider = ClusterProvider.GKE.value

    def get(self, path) -> dict:
        if not path:
            return {}
        if path[0] != '/':
            path = '/' + path
        print_info(f'GET {path}')

        try:
            return loads(self.api_client.call_api(path, 'GET', auth_settings=['BearerToken'], response_type='json', _preload_content=False)[0].data)
        except:
            print_error(f'Failed to get {path}')
            return None

    @classmethod
    def parse_data(self, raw_resources):
        parsed_output = {}

        for kind in raw_resources or {}:
            resources = {}
            resource_exists = False

            for raw_version in raw_resources[kind]:
                resource_items = raw_resources[kind][raw_version]
                if len(resource_items) == 0: continue

                resource_exists = True

                version = format_api_version(raw_version)
                resources[version] = {
                    'namespaced': False,
                    'namespaces': {},
                    'resources': {}
                }

                for item in resource_items:
                    metadata: dict = item['metadata']
                    name: str = metadata['name']
                    namespace: str = metadata.get('namespace')
                    formatted_id: str = format_resource_id(name, namespace)

                    formatted_data: dict = {
                        'json': dumps(item, indent=2, separators=(',', ': ')),
                        'yaml': safe_dump(item),
                        'data': item,
                        'metadata': metadata,
                        'stringified_metadata': safe_dump(metadata),
                        'stringified_data': {},
                        'stringified_annotations': safe_dump(metadata.get('annotations')) if metadata.get('annotations') else None,
                        'version': raw_version,
                        'kind': kind
                    }

                    del formatted_data['data']['metadata']
                    for key in formatted_data['data']:
                        formatted_data['stringified_data'][key] = safe_dump(formatted_data['data'][key])

                    owner_references = metadata.get('ownerReferences', [])
                    if len(owner_references) > 0:
                        formatted_data['ownerReferences'] = []
                        for ref in owner_references:
                            formatted_kind = format_resource_kind(ref['kind'])
                            formatted_version = format_api_version(ref['apiVersion'])
                            formatted_name = format_resource_name(ref['name'])

                            text = f'''{ref['apiVersion']}/{ref['kind']}/{ref['name']}'''
                            if namespace and ref['kind'] != 'Node':
                                formatted_name = format_resource_id(formatted_name, namespace)
                                text = f'''[{namespace}] ''' + text

                            formatted_data['ownerReferences'].append({
                                'href': f'''#services.{formatted_kind}.{formatted_version}.{formatted_name}.view'''.replace('"', '\\"'),
                                'text': text,
                            })

                    role_ref = item.get('roleRef')
                    if role_ref:
                        ref_api_group = role_ref.get('apiGroup')
                        ref_kind = role_ref.get('kind')
                        ref_name = role_ref.get('name')

                        ref_text = f'''{ref_api_group}/{ref_kind}/{ref_name}'''
                        if namespace:
                            ref_text = f'[{namespace}] {ref_text}'
                            ref_name = f'[{namespace}] {ref_name}'

                        ref_href = f'''#services.{format_resource_kind(ref_kind)}.{version}.{format_resource_id(ref_name, namespace)}.view'''
                        formatted_data['roleRef'] = {
                            'href': ref_href,
                            'text': ref_text,
                        }

                    resources[version]['resources'][formatted_id] = formatted_data
                    if namespace:
                        resources[version]['namespaced'] = True
                        resources[version]['namespaces'][format_resource_name(namespace)] = namespace

            if resource_exists:
                parsed_output[format_resource_kind(kind)] = resources

        return parsed_output