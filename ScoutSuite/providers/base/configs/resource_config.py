
class ResourceConfig(dict):

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        raise NotImplementedError()

    async def finalize(self):
        pass
