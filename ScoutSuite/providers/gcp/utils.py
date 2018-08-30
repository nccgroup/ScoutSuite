# -*- coding: utf-8 -*-

from opinel.utils.console import printException, printInfo

from google.cloud import storage

def connect_service(service, credentials, region_name = None):

    try:
        if service == 'cloudstorage':
            return storage.Client(credentials=credentials)
        else:
            printException('Service %s not supported' % service)
            return None

    except Exception as e:
        printException(e)
        return None
