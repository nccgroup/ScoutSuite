from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.core.console import print_exception


class NodePools(Resources):
    def __init__(self, cluster):
        super(NodePools, self).__init__(service_facade=None)
        self.cluster = cluster

    def fetch_all(self):
        raw_node_pools = self.cluster['nodePools']
        parsing_error_counter = 0
        for raw_node_pool in raw_node_pools:
            try:
                node_pool_id, node_pool = self._parse_node_pool(raw_node_pool)
                self[node_pool_id] = node_pool
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))
        # We need self.cluster to get the node pools, but we do 
        # not want to have it in the generated JSON.
        del self.cluster

    def _parse_node_pool(self, raw_node_pool):
        node_pool_dict = {}
        node_pool_dict['id'] = raw_node_pool['name']
        node_pool_dict['auto_repair_enabled'] = raw_node_pool.get('management', {}).get('autoRepair', False)
        node_pool_dict['auto_upgrade_enabled'] = raw_node_pool.get('management', {}).get('autoUpgrade', False)
        node_pool_dict['legacy_metadata_endpoints_enabled'] = self._is_legacy_metadata_endpoints_enabled(raw_node_pool)
        return node_pool_dict['id'], node_pool_dict

    def _is_legacy_metadata_endpoints_enabled(self, raw_node_pool):
        return raw_node_pool['config'].get('metadata', {}).get('disable-legacy-endpoints') == 'false'
