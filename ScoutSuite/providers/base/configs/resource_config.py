
class ResourceConfig(object):

    def __init__(self, thread_config=4):
        self._thread_config = thread_config

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        raise NotImplementedError()

    async def finalize(self):
        pass
