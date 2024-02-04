import boto3
from ScoutSuite.core.console import print_exception, print_debug, print_warning


def get_client(service: str, session: boto3.session.Session, region: str = None):
    """
    Instantiates an DO Spaces API client

    """

    try:
        return (
            session.client(
                service,
                region_name=region,
                endpoint_url="https://" + region + ".digitaloceanspaces.com",
            )
            if region
            else session.client(service)
        )
    except Exception as e:
        print_exception(f"Failed to create client for the {service} service: {e}")
        return None
