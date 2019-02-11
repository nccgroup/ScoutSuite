# -*- coding: utf-8 -*-

import re

from opinel.utils.console import printException, printInfo

from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.security import SecurityCenter

services = {
    'storageaccounts': StorageManagementClient,
    'monitor': MonitorManagementClient,
    'sqldatabase': SqlManagementClient,
    'securitycenter': lambda credentials, subscription_id: SecurityCenter(credentials, subscription_id, ''),
}

def azure_connect_service(service, credentials, region_name=None):
    try:
        #if service == 'storageaccounts':
        #    return StorageManagementClient(credentials.credentials, credentials.subscription_id)
        #elif service == 'monitor':
        #    return MonitorManagementClient(credentials.credentials, credentials.subscription_id)
        #elif service == 'sqldatabase':
        #    return SqlManagementClient(credentials.credentials, credentials.subscription_id)
        #elif service == 'securitycenter':
        #    return SecurityCenter(credentials.credentials, credentials.subscription_id, '')

        client = services.get(service)
        if client:
            return client(credentials.credentials, credentials.subscription_id)
        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None


def get_resource_group_name(id):
    return re.findall("/resourceGroups/(.*?)/", id)[0]
