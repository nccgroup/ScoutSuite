from ScoutSuite.providers.base.resources.base import Resources


class NodePools(Resources):
    def __init__(self, cluster):
        super(NodePools, self).__init__(service_facade=None)
        self.cluster = cluster

    def fetch_all(self):
        raw_node_pools = self.cluster['nodePools']
        for raw_node_pool in raw_node_pools:
            node_pool_id, node_pool = self._parse_node_pool(raw_node_pool)
            self[node_pool_id] = node_pool
        # We need self.cluster to get the node pools, but we do 
        # not want to have it in the generated JSON.
        del self.cluster

    def _parse_node_pool(self, raw_node_pool):
        node_pool_dict = {}
        node_pool_dict['id'] = raw_node_pool['name']
        node_pool_dict['status'] = raw_node_pool['status']
        node_pool_dict['auto_repair_enabled'] = \
            raw_node_pool.get('management', {}).get('autoRepair', False)
        node_pool_dict['auto_upgrade_enabled'] = \
            raw_node_pool.get('management', {}).get('autoUpgrade', False)
        node_pool_dict['secure_boot_enabled'] = \
            raw_node_pool.get('config', {}).get('shieldedInstanceConfig', {}).get('enableSecureBoot', False)
        node_pool_dict['integrity_monitoring_enabled'] = \
            raw_node_pool.get('config', {}).get('shieldedInstanceConfig', {}).get('enableIntegrityMonitoring', False)
        node_pool_dict['legacy_metadata_endpoints_enabled'] = \
            raw_node_pool['config'].get('metadata', {}).get('disable-legacy-endpoints') == 'false'
        return node_pool_dict['id'], node_pool_dict

