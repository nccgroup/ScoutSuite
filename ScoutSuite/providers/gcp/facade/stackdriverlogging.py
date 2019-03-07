from google.cloud import logging as stackdriver_logging

class StackdriverLoggingFacade:
    # TODO: Make truly async
    async def get_sinks(self, project_id):
        client = stackdriver_logging.Client(project=project_id)
        return [sink for sink in client.list_sinks()]
