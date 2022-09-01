from __future__ import print_function
from ScoutSuite import __version__

formatted_provider_name = {
    'aliyun': 'Aliyun',
    'aws': 'AWS',
    'azure': 'Azure',
    'gcp': 'GCP',
    'oci': 'OCI'
}

formatted_service_name = {
    # AWS
    'acm': 'ACM',
    'cloudformation': 'CloudFormation',
    'cloudtrail': 'CloudTrail',
    'cloudwatch': 'CloudWatch',
    'cloudfront': 'CloudFront',
    'credentials': 'Credentials',
    'codebuild': 'CodeBuild',
    'cognito': 'Cognito',
    'config': 'Config',
    'directconnect': 'Direct Connect',
    'dynamodb': 'DynamoDB',
    'ecr': 'ECR',
    'ecs': 'ECS',
    'elbv2': 'ELBv2',
    'eks': 'EKS',
    'elasticache': 'ElastiCache',
    'guardduty': 'GuardDuty',
    'lambda': 'Lambda',
    'awslambda': 'Lambda',
    'redshift': 'RedShift',
    'route53': 'Route53',
    'secretsmanager': 'Secrets Manager',
    'docdb': 'DocumentDB',
    'ssm': 'Systems Manager',
    # Azure
    'aad': 'Azure Active Directory',
    'rbac': 'Azure RBAC',
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
    'postgresqldatabase': 'PostgresSQL Database',
    'mysqldatabase': 'MySQL Database',
    'loggingmonitoring': 'Logging Monitoring',
    # GCP
    'cloudstorage': 'Cloud Storage',
    'cloudmemorystore': 'Cloud Memorystore',
    'memorystore': 'Cloud Memorystore',
    'cloudsql': 'Cloud SQL',
    'dns': 'DNS',
    'stackdriverlogging': 'Stackdriver Logging',
    'stackdrivermonitoring': 'Stackdriver Monitoring',
    'computeengine': 'Compute Engine',
    'kubernetesengine': 'Kubernetes Engine',
    'functions': 'Cloud Functions',
    'bigquery': 'BigQuery',
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


def format_provider_code(provider_code):
    """
    :param provider_code:
    :return:
    """
    return formatted_provider_name[provider_code] if provider_code in formatted_provider_name else provider_code.upper()


def format_service_name(service):
    """
    :param service:
    :return:
    """
    return formatted_service_name[service] if service in formatted_service_name else service.upper()


def get_user_agent():
    return 'Scout Suite/{} (https://github.com/nccgroup/ScoutSuite)'.format(__version__)
