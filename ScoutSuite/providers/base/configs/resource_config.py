
class ResourceConfig(object):
    def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        raise NotImplementedError()

    def finalize(self):
        raise NotImplementedError()