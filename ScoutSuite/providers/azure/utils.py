# -*- coding: utf-8 -*-

from opinel.utils.console import printException, printInfo

from azure.mgmt.storage import StorageManagementClient

def azure_connect_service(service, credentials, region_name=None):

    try:
        if service == 'storageaccounts':
            return StorageManagementClient(credentials.credentials, credentials.subscription_id)

        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None
