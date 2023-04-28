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


def is_throttled(exception):
    """
    Determines whether the exception is due to API throttling.

    :param exception:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    # taken from botocore.retries.standard.ThrottledRetryableChecker
    throttled_errors = [
        'Throttling',
        'ThrottlingException',
        'ThrottledException',
        'RequestThrottledException',
        'TooManyRequestsException',
        'ProvisionedThroughputExceededException',
        'TransactionInProgressException',
        'RequestLimitExceeded',
        'BandwidthLimitExceeded',
        'LimitExceededException',
        'RequestThrottled',
        'SlowDown',
        'PriorRequestNotComplete',
        'EC2ThrottledException',
    ]

    try:
        throttled = (hasattr(exception, "response")
                     and exception.response
                     and "Error" in exception.response
                     and exception.response["Error"]["Code"] in throttled_errors) \
                    or \
                    any(error in str(exception) for error in throttled_errors)
        return throttled
    except Exception as e:
        print_exception(f'Unable to validate exception {exception} for AWS throttling: {e}')
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


def format_arn(partition, service, region, account_id, resource_id, resource_type=None):
    """
    Formats a resource ARN based on the parameters

    :param partition:                   The partition where the resource is located
    :param service:                     The service namespace that identified the AWS product
    :param region:                      The corresponding region
    :param account_id:                  The ID of the AWS account that owns the resource
    :param resource_id:                 The resource identified
    :param resource_type:               (Optional) The resource type
    :return:                            Resource ARN
    """

    try:
        # If a resource type is specified
        if resource_type is not None:
            arn = f"arn:{partition}:{service}:{region}:{account_id}:{resource_type}/{resource_id}"
        else:
            arn = f"arn:{partition}:{service}:{region}:{account_id}:{resource_id}"
    except Exception as e:
        print_exception(f'Failed to parse a resource ARN: {e}')
        return None
    return arn
