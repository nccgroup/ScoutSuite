from __future__ import print_function

formatted_service_name = {
    # AWS
    'acm': 'ACM',
    'cloudformation': 'CloudFormation',
    'cloudtrail': 'CloudTrail',
    'cloudwatch': 'CloudWatch',
    'credentials': 'Credentials',
    'config': 'Config',
    'directconnect': 'Direct Connect',
    'dynamodb': 'DynamoDB',
    'elbv2': 'ELBv2',
    'elasticache': 'ElastiCache',
    'lambda': 'Lambda',
    'awslambda': 'Lambda',
    'redshift': 'RedShift',
    'route53': 'Route53',
    'secretsmanager': 'Secrets Manager',
    # Azure
    'storageaccounts': 'Storage Accounts',
    'sqldatabase': 'SQL Database',
    'securitycenter': 'Security Center',
    'keyvault': 'Key Vault',
    'appgateway': 'Application Gateway',
    'rediscache': 'Redis Cache',
    'network': 'Network',
    'appservice': 'App Services',
    'loadbalancer': 'Load Balancer',
    'virtualmachines': 'Virtual Machines',
    # GCP
    'cloudstorage': 'Cloud Storage',
    'cloudsql': 'Cloud SQL',
    'stackdriverlogging': 'Stackdriver Logging',
    'stackdrivermonitoring': 'Stackdriver Monitoring',
    'computeengine': 'Compute Engine',
    'kubernetesengine': 'Kubernetes Engine',
    'cloudresourcemanager': 'Cloud Resource Manager',
    # Aliyun
    'actiontrail': 'ActionTrail',
    # OCI
    'identity': 'Identity',
    'objectstorage': 'Object Storage',
}


def manage_dictionary(dictionary, key, init, callback=None):
    """
    :param dictionary:
    :param key:
    :param init:
    :param callback:
    :return:
    """
    if not isinstance(dictionary, dict):
        raise TypeError()

    if str(key) in dictionary:
        return dictionary

    dictionary[str(key)] = init
    manage_dictionary(dictionary, key, init)
    if callback:
        callback(dictionary[key])
    return dictionary


def format_service_name(service):
    """

    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()
