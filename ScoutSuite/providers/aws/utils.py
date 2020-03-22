import re
from ScoutSuite.core.console import print_exception

ec2_classic = 'EC2-Classic'


def get_caller_identity(session):
    sts_client = session.client('sts')
    identity = sts_client.get_caller_identity()
    return identity


def get_aws_account_id(session):
    caller_identity = get_caller_identity(session)
    account_id = caller_identity['Arn'].split(':')[4]
    return account_id


def get_partition_name(session):
    caller_identity = get_caller_identity(session)
    partition_name = caller_identity['Arn'].split(':')[1]
    return partition_name


def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    try:
        return (hasattr(e, 'response')
                and e.response
                and 'Error' in e.response
                and e.response['Error']['Code'] in ['Throttling',
                                                    'RequestLimitExceeded',
                                                    'ThrottlingException'])
    except Exception as e:
        print_exception('Unable to validate exception for throttling: {}'.format(e))
        return False


def get_keys(src, dst, keys):
    """
    Copies the value of keys from source object to dest object

    :param src:                         Source object
    :param dst:                         Destination object
    :param keys:                        Keys
    :return:
    """
    for key in keys:
        dst[key] = src[key] if key in src else None


def get_name(src, dst, default_attribute):
    """

    :param src:                         Source object
    :param dst:                         Destination object
    :param default_attribute:           Default attribute

    :return:
    """
    name_found = False
    if 'Tags' in src:
        for tag in src['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] != '':
                dst['name'] = tag['Value']
                name_found = True
    if not name_found:
        dst['name'] = src[default_attribute]
    return dst['name']


def no_camel(name):
    """
    Converts CamelCase to camel_case

    :param name:                        Name string to convert
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
