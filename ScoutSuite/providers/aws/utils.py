import re
from ScoutSuite.core.console import print_exception

ec2_classic = "EC2-Classic"


def get_caller_identity(session):
    sts_client = session.client("sts")
    identity = sts_client.get_caller_identity()
    return identity


def get_aws_account_id(session):
    caller_identity = get_caller_identity(session)
    account_id = caller_identity["Arn"].split(":")[4]
    return account_id


def get_partition_name(session):
    caller_identity = get_caller_identity(session)
    partition_name = caller_identity["Arn"].split(":")[1]
    return partition_name


def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    try:
        return (
            hasattr(e, "response")
            and e.response
            and "Error" in e.response
            and e.response["Error"]["Code"]
            in ["Throttling", "RequestLimitExceeded", "ThrottlingException"]
        )
    except Exception as e:
        print_exception(f'Unable to validate exception for throttling: {e}')
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
    if "Tags" in src:
        for tag in src["Tags"]:
            if tag["Key"] == "Name" and tag["Value"] != "":
                dst["name"] = tag["Value"]
                name_found = True
    if not name_found:
        dst["name"] = src[default_attribute]
    return dst["name"]

async def set_tags(raw_instance: {}):
    if 'Tags' in raw_instance:
        instance = {x['Key']: x['Value'] for x in raw_instance['Tags']}
    else:
        instance = {}
    return instance
    
def no_camel(name):
    """
    Converts CamelCase to camel_case

    :param name:                        Name string to convert
    :return:
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_keys(d):
    """
    Converts a dictionary with CamelCase keys to camel_case

    :param name:                        d Dictionary to iterate over
    :return:
    """

    new_table = {}
    if isinstance(d, dict):
        for k in d.keys():
            new_key = no_camel(k)
            if isinstance(d[k], dict):
                new_table[new_key] = snake_keys(d[k])
            elif isinstance(d[k], list):
                new_ary = []
                for v in d[k]:
                    if isinstance(v, dict):
                        new_ary.append(snake_keys(v))
                    else:
                        new_ary.append(v)
                new_table[new_key] = new_ary
            else:
                new_table[new_key] = d[k]
    return new_table
