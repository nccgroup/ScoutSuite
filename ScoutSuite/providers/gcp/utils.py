from ScoutSuite.core.console import print_exception

def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    try:
        if 'Quota exceeded' in str(e):
            return True
        else:
            return False
    except Exception as e:
        print_exception(f'Unable to validate exception for throttling: {e}')
        return False
