
class ResourceConfig(dict):

    async def fetch_all(self, **kwargs):
        raise NotImplementedError()

    async def finalize(self):
        pass
