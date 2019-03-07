# -*- coding: utf-8 -*-

from google.cloud import storage

class CloudStorageFacade:
    def __init__(self):
        self._cloudstorage_client = storage.Client()

    # TODO: Make truly async
    async def get_buckets(self, project_id):
        return self._cloudstorage_client.list_buckets(project=project_id)