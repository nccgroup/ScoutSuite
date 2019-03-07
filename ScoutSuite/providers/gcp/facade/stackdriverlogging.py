# -*- coding: utf-8 -*-

from google.cloud import logging as stackdriver_logging

class StackdriverLoggingFacade:
    # TODO: Make truly async
    async def get_sinks(self, project_id):
        client = stackdriver_logging.Client(project=project_id)
        return client.list_sinks()
