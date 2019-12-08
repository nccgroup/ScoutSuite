from oci.identity import IdentityClient

from ScoutSuite.core.console import print_exception


def oracle_connect_service(service, credentials, region_name=None):
    try:
        if service == 'identity':
            return IdentityClient(credentials.config)
        else:
            print_exception('Service %s not supported' % service)
            return None

    except Exception as e:
        print_exception(e)
        return None
