from ScoutSuite.core.console import print_exception

def is_throttled(exception):
    """
    Determines whether the exception is due to API throttling.

    :param exception:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    try:
        if 'Quota exceeded' in str(exception):
            return True
        else:
            return False
    except Exception as exception:
        print_exception(f'Unable to validate exception {e} for GCP throttling: {exception}')
        return False
