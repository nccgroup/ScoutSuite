from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id


class RedisInstances(GCPCompositeResources):

    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_instances = await self.facade.memorystoreredis.get_redis_instances(self.project_id)
        for raw_instance in raw_instances:
            instance_id, instance = self._parse_instance(raw_instance)
            self[instance_id] = instance

    def _parse_instance(self, raw_instance):
        instance_dict = {}

        instance_dict['id'] = get_non_provider_id(raw_instance['name'])
        instance_dict['name'] = raw_instance.get('displayName')
        instance_dict['project_id'] = self.project_id
        instance_dict['location'] = raw_instance['locationId']
        instance_dict['redis_version'] = raw_instance['redisVersion']
        instance_dict['port'] = raw_instance['port']
        instance_dict['tier'] = raw_instance['tier']
        instance_dict['memory_size_gb'] = raw_instance['memorySizeGb']
        instance_dict['authorized_network'] = raw_instance['authorizedNetwork']
        instance_dict['connect_mode'] = raw_instance['connectMode']
        instance_dict['transit_encryption_mode'] = raw_instance['transitEncryptionMode']
        instance_dict['ssl_required'] = self._is_ssl_required(raw_instance)
        instance_dict['auth_enabled'] = self._is_auth_required(raw_instance)

        return instance_dict['id'], instance_dict

    def _is_ssl_required(self, raw_instance):
        # Checks if transit encryption mode is SERVER_AUTHENTICATION. Otherwise, SSL
        # is not enabled.
        is_ssl_required = raw_instance.get('transitEncryptionMode', False)
        if is_ssl_required == 'SERVER_AUTHENTICATION':
            return True
        return False

    def _is_auth_required(self, raw_instance):
        is_auth_enabled = raw_instance.get('authEnabled', False)
        return is_auth_enabled

