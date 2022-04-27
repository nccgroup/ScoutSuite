from ScoutSuite.core.console import print_exception


def is_throttled(exception):
    """
    Determines whether the exception is due to API throttling.

    :param exception:                   Exception raised
    :return:                            True if it's a throttling exception else False
    """
    throttled_errors = [
        'Quota exceeded',
        'API_SHARED_QUOTA_EXHAUSTED',
        'RATE_LIMIT_EXCEEDED'
    ]
    try:
        if any(error in str(exception) for error in throttled_errors):
            return True
        else:
            return False
    except Exception as e:
        print_exception(f'Unable to validate exception {exception} for GCP throttling: {e}')
        return False
