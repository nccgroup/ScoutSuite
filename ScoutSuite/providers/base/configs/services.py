



class BaseServicesConfig:

    def __init__(self, metadata, thread_config = 4):
        pass

    def fetch(self, credentials, services = [], regions = [], partition_name = ''):
        pass

    def postprocessing(self):
        pass
