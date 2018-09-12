# -*- coding: utf-8 -*-

from opinel.utils.console import printException, printInfo

from google.cloud import storage

from googleapiclient import discovery

def gcp_connect_service(service, credentials, region_name=None):

    try:
        if service == 'cloudstorage':

            # return storage.Client(credentials=credentials.cloud_client_credentials)
            return storage.Client(credentials=credentials)

        elif service == 'cloudsql':

            # client = discovery.build('sqladmin', 'v1beta4', credentials.api_client_credentials)
            # return client

            # TODO not sure why this works - there are no credentials for API client libraries
            return discovery.build('sqladmin', 'v1beta4')

        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None
