from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.memorystore.redis_instances import RedisInstances


class MemoryStore(Projects):
    _children = [ 
        (RedisInstances, 'redis_instances')
     ]
