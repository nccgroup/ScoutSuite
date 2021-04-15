import unittest
from unittest import mock

import pytest

from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.base.authentication_strategy import AuthenticationException
from ScoutSuite.providers.base.authentication_strategy_factory import get_authentication_strategy


# Test methods for Azure Provider
class TestAzureProviderClass(unittest.TestCase):
    @mock.patch("ScoutSuite.providers.azure.authentication_strategy.UsernamePasswordCredential")
    def test_authenticate(self, mock_UsernamePasswordCredential):
        azure_authentication_strategy = get_authentication_strategy("azure")

        result = azure_authentication_strategy.authenticate(
            user_account=True,
            client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46',
            tenant_id='some-tenant-id',
            username='some-username',
            password='some-password',
            authority='https://login.microsoftonline.com/'
        )

        mock_UsernamePasswordCredential.assert_called_with('04b07795-8ddb-461a-bbee-02f9e1bf7b46', 'some-username',
                                                          'some-password',
                                                           authority='https://login.microsoftonline.com/',
                                                           tenant_id='some-tenant-id')
        assert isinstance(result, AzureCredentials)

        # exception test
        with pytest.raises(AuthenticationException):
            result = azure_authentication_strategy.authenticate(None, None, None, None)

    @mock.patch("ScoutSuite.providers.azure.authentication_strategy.AzureCliCredential")
    def test_authenticate_CLI(self, mock_AzureCliCredential):
        azure_authentication_strategy = get_authentication_strategy("azure")

        result = azure_authentication_strategy.authenticate(
            cli=True,
            client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46',
            authority='https://login.microsoftonline.com/'
        )

        mock_AzureCliCredential.assert_called_with()
        assert isinstance(result, AzureCredentials)

        # exception test
        with pytest.raises(AuthenticationException):
            result = azure_authentication_strategy.authenticate(None, None, None, None)
