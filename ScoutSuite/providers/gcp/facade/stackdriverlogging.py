# -*- coding: utf-8 -*-

from google.cloud import logging as stackdriver_logging

class StackdriverLoggingFacade:
    def get_sinks(project_id):
        client = stackdriver_logging.Client(project=project_id)
        return client.list_sinks()
