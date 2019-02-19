# -*- coding: utf-8 -*-

import re

from opinel.utils.console import printException, printInfo

from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.sql import SqlManagementClient

from azure.mgmt.security import SecurityCenter
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.web import WebSiteManagementClient


def azure_connect_service(service, credentials, region_name=None):
    try:
        if service == 'storageaccounts':
            return StorageManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'monitor':
            return MonitorManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'sqldatabase':
            return SqlManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'keyvault':
            return KeyVaultManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'appgateway':
            return NetworkManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'network':
            return NetworkManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'rediscache':
            return RedisManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'securitycenter':
            return SecurityCenter(credentials.credentials, credentials.subscription_id, '')
        elif service == 'appservice':
            return WebSiteManagementClient(credentials.credentials, credentials.subscription_id)
        elif service == 'loadbalancer':
            return NetworkManagementClient(credentials.credentials, credentials.subscription_id)
        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None


def get_resource_group_name(id):
    return re.findall("/resourceGroups/(.*?)/", id)[0]
