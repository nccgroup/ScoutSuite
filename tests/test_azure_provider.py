import unittest
from unittest import mock

import pytest

from ScoutSuite.providers.azure.authentication_strategy import AzureCredentials
from ScoutSuite.providers.base.authentication_strategy import AuthenticationException
from ScoutSuite.providers.base.authentication_strategy_factory import get_authentication_strategy


# Test methods for Azure Provider
class TestAzureProviderClass(unittest.TestCase):
    @mock.patch("ScoutSuite.providers.azure.authentication_strategy.UserPassCredentials")
    def test_authenticate(self, mock_UserPassCredentials):
        azure_authentication_strategy = get_authentication_strategy("azure")

        result = azure_authentication_strategy.authenticate(
            user_account=True,
            username='some-username',
            password='some-password'
        )

        mock_UserPassCredentials.assert_called_with('some-username', 'some-password',
                                                    resource='https://graph.windows.net')
        assert isinstance(result, AzureCredentials)

        # exception test
        with pytest.raises(AuthenticationException):
            result = azure_authentication_strategy.authenticate(None, None, None, None)
