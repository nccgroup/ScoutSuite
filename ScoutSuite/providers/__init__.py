providers_dict = {'aws': 'AWSProvider',
                  'gcp': 'GCPProvider',
                  'azure': 'AzureProvider',
                  'aliyun': 'AliyunProvider',
                  'oci': 'OracleProvider'}


def get_provider_object(provider):
    provider_class = providers_dict.get(provider)
    provider_module = __import__(f'ScoutSuite.providers.{provider}.provider', fromlist=[provider_class])
    provider_object = getattr(provider_module, provider_class)
    return provider_object


def get_provider(provider,
                 profile=None,
                 project_id=None, folder_id=None, organization_id=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):
    """
    Returns an instance of the requested provider.

    :param profile:             The name of the profile desired
    :param project_id:          The identifier of the project
    :param folder_id:           The identifier of the folder
    :param organization_id:     The identifier of the organization
    :param report_dir:          Where to save the report
    :param timestamp:           Whether to print or not the timestamp on the report
    :param services:            Exclusive list of services on which to run Scout Suite
    :param skipped_services:    List of services not to run Scout Suite on
    :param provider:            A string indicating the provider
    :return:                    A child instance of the BaseProvider class or None if no object implemented
    """
    services = [] if services is None else services
    skipped_services = [] if skipped_services is None else skipped_services

    provider_object = get_provider_object(provider)
    provider_instance = provider_object(profile=profile,
                                        project_id=project_id,
                                        folder_id=folder_id,
                                        organization_id=organization_id,
                                        report_dir=report_dir,
                                        timestamp=timestamp,
                                        services=services,
                                        skipped_services=skipped_services,
                                        **kwargs)

    return provider_instance
