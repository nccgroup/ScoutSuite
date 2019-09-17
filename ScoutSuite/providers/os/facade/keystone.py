from ScoutSuite.providers.os.authentication_strategy import OpenstackCredentials


class KeystoneFacade:
    def __init__(self, credentials: OpenstackCredentials):
        self._credentials = credentials

    def is_fernet(self):
        # TODO Fernet test - implement a better way to test if fernet tokens are used
        return self._credentials.session.auth_token[0:6] == 'gAAAAA'
