from ScoutSuite.providers.salesforce.authentication_strategy import SalesforceCredentials


class SalesforceFacade:
    def __init__(self, credentials: SalesforceCredentials):
        self._credentials = credentials
        self._instantiate_facades()

    def _instantiate_facades(self):
        pass
