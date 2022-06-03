from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.gke.node_pools import NodePools
from ScoutSuite.providers.utils import get_non_provider_id


class Clusters(Resources):
    def __init__(self, facade: GCPFacade, project_id):
        super(Clusters, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_clusters = await self.facade.gke.get_clusters(self.project_id)
        for raw_cluster in raw_clusters:
            cluster_id, cluster = await self._parse_cluster(raw_cluster)
            self[cluster_id] = cluster
            self[cluster_id]['node_pools'].fetch_all()

    async def _parse_cluster(self, raw_cluster):
        cluster_dict = {}
        cluster_dict['id'] = get_non_provider_id(raw_cluster['name'])
        cluster_dict['name'] = raw_cluster['name']
        cluster_dict['location'] = raw_cluster['location']
        cluster_dict['status'] = raw_cluster['status']
        cluster_dict['type'] = "Zonal" if raw_cluster['location'].count("-") > 1 else "Regional"
        cluster_dict['alias_ip_enabled'] = raw_cluster.get('ipAllocationPolicy', {}).get('useIpAliases', False)
        cluster_dict['basic_authentication_enabled'] = self._is_basic_authentication_enabled(raw_cluster)
        cluster_dict['client_certificate_enabled'] = self._is_client_certificate_enabled(raw_cluster)
        cluster_dict['pod_security_policy_enabled'] = self._is_pod_security_policy_enabled(raw_cluster)
        cluster_dict['dashboard_status'] = self._get_dashboard_status(raw_cluster)
        cluster_dict['has_limited_scopes'] = self._has_limited_scopes(raw_cluster)
        cluster_dict['image_type'] = raw_cluster.get('nodeConfig', {}).get('imageType', None)
        cluster_dict['labels'] = raw_cluster.get('resourceLabels', [])
        cluster_dict['has_labels'] = len(cluster_dict['labels']) > 0
        cluster_dict['endpoint'] = raw_cluster.get('endpoint')
        cluster_dict['legacy_abac_enabled'] = raw_cluster.get('legacyAbac', {}).get('enabled', False)
        cluster_dict['logging_enabled'] = self._is_logging_enabled(raw_cluster)
        cluster_dict['master_authorized_networks_enabled'] = raw_cluster.get('masterAuthorizedNetworksConfig', {}).get('enabled', False)
        cluster_dict['monitoring_enabled'] = self._is_monitoring_enabled(raw_cluster)
        cluster_dict['network_policy_enabled'] = raw_cluster.get('networkPolicy', {}).get('enabled', False)
        cluster_dict['node_pools'] = NodePools(raw_cluster)
        cluster_dict['scopes'] = self._get_scopes(raw_cluster)
        cluster_dict['service_account'] = raw_cluster.get('nodeConfig', {}).get('serviceAccount', None)
        cluster_dict['master_authorized_networks_config'] = self._get_master_authorized_networks_config(raw_cluster)
        cluster_dict['application_layer_encryption_enabled'] = raw_cluster.get('databaseEncryption', {}).get('state', None) == 'ENCRYPTED'
        cluster_dict['workload_identity_enabled'] = raw_cluster.get('workloadIdentityConfig', {}).get('identityNamespace', None) != None
        cluster_dict['metadata_server_enabled'] = self._metadata_server_enabled(raw_cluster.get('nodePools', []))
        cluster_dict['release_channel'] = raw_cluster.get('releaseChannel', {}).get('channel', None)
        cluster_dict['shielded_nodes_enabled'] = raw_cluster.get('shieldedNodes', {}).get('enabled', False)
        cluster_dict['binary_authorization_enabled'] = raw_cluster.get('binaryAuthorization', {}).get('enabled', False)
        cluster_dict['private_ip_google_access_enabled'] = raw_cluster.get('privateIpGoogleAccess', False)
        cluster_dict['private_nodes_enabled'] = raw_cluster.get('privateClusterConfig', {}).get('enablePrivateNodes', False)
        cluster_dict['private_endpoint_enabled'] = raw_cluster.get('privateClusterConfig', {}).get('enablePrivateEndpoint', False)
        cluster_dict['public_endpoint'] = raw_cluster.get('privateClusterConfig', {}).get('publicEndpoint', None)
        cluster_dict['private_endpoint'] = raw_cluster.get('privateClusterConfig', {}).get('privateEndpoint', None)

        return cluster_dict['id'], cluster_dict

    def _metadata_server_enabled(self, node_pools):
        for pool in node_pools:
            if pool.get('config', {}).get('workloadMetadataConfig', {}) == {}:
                return False
        return True

    def _get_master_authorized_networks_config(self, raw_cluster):
        if raw_cluster.get('masterAuthorizedNetworksConfig'):
            config = raw_cluster.get('masterAuthorizedNetworksConfig')
            config['includes_public_cidr'] = False
            for block in config.get('cidrBlocks', []):
                if block.get('cidrBlock') == '0.0.0.0/0':
                    config['includes_public_cidr'] = True
            return config
        else:
            return {
                'enabled': False,
                'cidrBlocks': [],
                'includes_public_cidr': False
            }

    def _is_pod_security_policy_enabled(self, raw_cluster):
        if 'podSecurityPolicyConfig' in raw_cluster:
            return raw_cluster['podSecurityPolicyConfig'].get('enabled', False)
        return False

        return raw_cluster['masterAuth'].get('username', '') != ''

    def _is_basic_authentication_enabled(self, raw_cluster):
        return raw_cluster['masterAuth'].get('username', '') != ''

    def _is_client_certificate_enabled(self, raw_cluster):
        return raw_cluster['masterAuth'].get('clientCertificate', '') != ''

    def _is_logging_enabled(self, raw_cluster):
        return raw_cluster['loggingService'] != 'none'

    def _is_monitoring_enabled(self, raw_cluster):
        return raw_cluster['monitoringService'] != 'none'

    def _parse_scope(self, scope_url):
        return scope_url.split('/')[-1]

    def _get_scopes(self, raw_cluster):
        return [self._parse_scope(scope_url) for scope_url in raw_cluster['nodeConfig'].get('oauthScopes', [])]

    def _has_limited_scopes(self, raw_cluster):
        minimum_scopes = {'devstorage.read_only', 'logging.write', 'monitoring'}
        cluster_scopes = self._get_scopes(raw_cluster)
        return all(scope in minimum_scopes for scope in cluster_scopes)

    def _get_dashboard_status(self, raw_cluster):
        is_disabled = 'kubernetesDashboard' not in raw_cluster['addonsConfig'] or \
                      raw_cluster['addonsConfig']['kubernetesDashboard'].get('disabled')
        return 'Disabled' if is_disabled else 'Enabled'
