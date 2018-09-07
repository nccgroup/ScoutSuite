# -*- coding: utf-8 -*-

from opinel.utils.console import printException, printInfo

from google.cloud import storage

from googleapiclient import discovery

def gcp_connect_service(service, credentials, region_name=None):

    try:
        if service == 'cloudstorage':

            # service = discovery.build('storage', 'v1', credentials)

            return storage.Client(credentials=credentials)

        # elif service == 'cloudsql':

        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None

"""
insert_entity(projectId, "storage", ["buckets"], "Bucket")
insert_entity(projectId, "sqladmin", ["instances"], "SQL Instance", "v1beta4")
"""
def insert_entity(projectId, product, categories, table_name, version="v1", prefix="", items="items"):

    service = discovery.build(product, version, credentials=storage.get())
    while categories:
        api_entity = getattr(service, categories.pop(0))()
        service = api_entity
    request = api_entity.list(project=prefix + projectId)
    try:
        while request is not None:
            response = request.execute()
            for item in response[items]:
                db.table(table_name).insert(item)
            try:
                request = api_entity.list_next(previous_request=request, previous_response=response)
            except AttributeError:
                request = None
    except KeyError:
        pass
