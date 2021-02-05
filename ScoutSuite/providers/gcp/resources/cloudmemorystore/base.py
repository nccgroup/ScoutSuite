from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.cloudmemorystore.redis_instances import RedisInstances

class CloudMemorystore(Projects):
    _children = [ 
        (RedisInstances, 'redis_instances')
     ]
