import sys
import unittest
from unittest.mock import patch, MagicMock

import pytest

from google.auth import compute_engine
import google.oauth2.service_account

from ScoutSuite.providers.gcp.authentication_strategy import GCPAuthenticationStrategy
from ScoutSuite.providers.base.authentication_strategy import AuthenticationException
from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser


class TestGCPAuthenticationStrategy(unittest.TestCase):
    """Unit tests for GCPAuthenticationStrategy.authenticate()."""

    # ------------------------------------------------------------------
    # Helper: build a fresh strategy instance (no real auth needed)
    # ------------------------------------------------------------------
    def _strategy(self):
        return GCPAuthenticationStrategy()

    # ------------------------------------------------------------------
    # Verify user account mode calls google.auth.default() and marks
    # credentials as a non-service-account with the project ID attached
    # ------------------------------------------------------------------
    def test_authenticate_user_account(self):
        """user_account=True calls auth.default() once; is_service_account=False; default_project_id attached."""
        mock_creds = MagicMock()
        mock_project = 'test-project-123'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_creds, mock_project)
        ) as mock_default:
            strategy = self._strategy()
            result = strategy.authenticate(user_account=True)

        mock_default.assert_called_once()
        self.assertFalse(result.is_service_account)
        self.assertEqual(result.default_project_id, mock_project)

    # ------------------------------------------------------------------
    # Verify service account key file mode calls google.auth.default(),
    # sets is_service_account=True, and attaches the project ID
    # ------------------------------------------------------------------
    def test_authenticate_service_account(self):
        """service_account=path calls auth.default() once; is_service_account=True; default_project_id attached."""
        mock_creds = MagicMock()
        mock_project = 'test-project-sa'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_creds, mock_project)
        ) as mock_default, \
             patch('os.path.abspath', return_value='/fake/path/key.json'), \
             patch.dict('os.environ', {}, clear=False):
            strategy = self._strategy()
            result = strategy.authenticate(service_account='/fake/path/key.json')

        mock_default.assert_called_once()
        self.assertTrue(result.is_service_account)
        self.assertEqual(result.default_project_id, mock_project)

    # ------------------------------------------------------------------
    # Verify ADC mode calls google.auth.default() exactly once and
    # attaches the project ID returned by the library
    # ------------------------------------------------------------------
    def test_authenticate_adc(self):
        """adc=True calls auth.default() once; default_project_id attached."""
        mock_creds = MagicMock()
        mock_project = 'test-project-adc'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_creds, mock_project)
        ) as mock_default:
            strategy = self._strategy()
            result = strategy.authenticate(adc=True)

        mock_default.assert_called_once()
        self.assertEqual(result.default_project_id, mock_project)

    # ------------------------------------------------------------------
    # Verify ADC mode on GCE/Cloud Run/GKE: when the metadata server
    # returns compute_engine.Credentials, is_service_account is True
    # and the service account email is preserved on the credentials object
    # ------------------------------------------------------------------
    def test_authenticate_adc_on_compute_engine(self):
        """adc=True with compute_engine.Credentials → is_service_account=True; service_account_email preserved."""
        mock_ce_creds = MagicMock(spec=compute_engine.Credentials)
        mock_ce_creds.service_account_email = 'sa@project.iam.gserviceaccount.com'
        mock_project = 'test-project-ce'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_ce_creds, mock_project)
        ):
            strategy = self._strategy()
            result = strategy.authenticate(adc=True)

        self.assertTrue(result.is_service_account)
        self.assertEqual(result.service_account_email, 'sa@project.iam.gserviceaccount.com')
        self.assertEqual(result.default_project_id, mock_project)

    # ------------------------------------------------------------------
    # Verify ADC mode correctly identifies a service account credential
    # when GOOGLE_APPLICATION_CREDENTIALS points to a SA key file and
    # google.auth.default() returns oauth2.service_account.Credentials
    # ------------------------------------------------------------------
    def test_authenticate_adc_with_service_account_credentials(self):
        """adc=True with oauth2.service_account.Credentials → is_service_account=True."""
        mock_sa_creds = MagicMock(spec=google.oauth2.service_account.Credentials)
        mock_project = 'test-project-sa-creds'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_sa_creds, mock_project)
        ):
            strategy = self._strategy()
            result = strategy.authenticate(adc=True)

        self.assertTrue(result.is_service_account)

    # ------------------------------------------------------------------
    # Verify ADC mode with any other credential type (e.g. gcloud user
    # OAuth credentials) is correctly marked as non-service-account
    # ------------------------------------------------------------------
    def test_authenticate_adc_with_other_credentials(self):
        """adc=True with generic credentials (not CE or SA) → is_service_account=False."""
        mock_other_creds = MagicMock()
        mock_project = 'test-project-other'

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_other_creds, mock_project)
        ):
            strategy = self._strategy()
            result = strategy.authenticate(adc=True)

        self.assertFalse(result.is_service_account)

    # ------------------------------------------------------------------
    # Verify that calling authenticate() without any auth mode flag
    # raises AuthenticationException with a clear message rather than
    # silently proceeding or raising an unrelated error
    # ------------------------------------------------------------------
    def test_authenticate_no_mode_raises(self):
        """No mode flags → AuthenticationException with correct message."""
        strategy = self._strategy()
        with self.assertRaises(AuthenticationException) as ctx:
            strategy.authenticate()

        self.assertIn('no supported account type', str(ctx.exception))

    # ------------------------------------------------------------------
    # Verify that ADC mode raises AuthenticationException when
    # google.auth.default() returns no credentials — this covers running
    # outside GCP with no gcloud ADC configured
    # ------------------------------------------------------------------
    def test_authenticate_adc_no_credentials_raises(self):
        """adc=True with auth.default() returning (None, None) → AuthenticationException."""
        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(None, None)
        ):
            strategy = self._strategy()
            with self.assertRaises(AuthenticationException):
                strategy.authenticate(adc=True)


class TestGCPCLIParser(unittest.TestCase):
    """Unit tests for ScoutSuiteArgumentParser GCP subcommand."""

    def _parser(self):
        return ScoutSuiteArgumentParser()

    # ------------------------------------------------------------------
    # Verify the --adc flag is recognised by the GCP subcommand parser
    # and results in adc=True in the parsed argument namespace
    # ------------------------------------------------------------------
    def test_cli_adc_flag_accepted(self):
        """--adc on CLI sets args['adc'] = True."""
        parser = self._parser()
        args = parser.parse_args(['gcp', '--adc'])
        self.assertTrue(args.__dict__['adc'])

    # ------------------------------------------------------------------
    # Verify adc defaults to False when no authentication mode flag is
    # given, preserving backward-compatible behaviour for existing callers
    # ------------------------------------------------------------------
    def test_cli_adc_default_false(self):
        """No auth flag defaults adc to False; using -u to satisfy required group."""
        parser = self._parser()
        args = parser.parse_args(['gcp', '-u'])
        self.assertFalse(args.__dict__.get('adc', False))

    # ------------------------------------------------------------------
    # Verify --adc and -u cannot be used together — argparse should
    # reject the combination and exit with a non-zero status code
    # ------------------------------------------------------------------
    def test_cli_adc_mutex_with_user_account(self):
        """--adc combined with -u → SystemExit."""
        parser = self._parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['gcp', '--adc', '-u'])

    # ------------------------------------------------------------------
    # Verify --adc and -s cannot be used together — argparse should
    # reject the combination and exit with a non-zero status code
    # ------------------------------------------------------------------
    def test_cli_adc_mutex_with_service_account(self):
        """--adc combined with -s key.json → SystemExit."""
        parser = self._parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['gcp', '--adc', '-s', 'key.json'])

    # ------------------------------------------------------------------
    # Verify the --adc help text mentions the three GCP environments
    # where ADC is the recommended authentication approach
    # ------------------------------------------------------------------
    def test_cli_adc_help_string(self):
        """Help text for --adc contains 'GCE', 'Cloud Run', and 'GKE'."""
        parser = self._parser()
        # Retrieve the GCP subparser and find the --adc action's help string
        gcp_subparser = None
        for action in parser.parser._subparsers._group_actions:
            if hasattr(action, '_name_parser_map') and 'gcp' in action._name_parser_map:
                gcp_subparser = action._name_parser_map['gcp']
                break

        self.assertIsNotNone(gcp_subparser, "GCP subparser not found")

        adc_help = None
        for action in gcp_subparser._actions:
            if '--adc' in getattr(action, 'option_strings', []):
                adc_help = action.help
                break

        self.assertIsNotNone(adc_help, "--adc action not found in GCP subparser")
        self.assertIn('GCE', adc_help)
        self.assertIn('Cloud Run', adc_help)
        self.assertIn('GKE', adc_help)


class TestGCPBackwardCompatibility(unittest.TestCase):
    """Tests that existing -u and -s authentication modes are unaffected by the --adc addition."""

    def _parser(self):
        return ScoutSuiteArgumentParser()

    # ------------------------------------------------------------------
    # Verify -u (user account) still works exactly as before — existing
    # workflows passing -u should not be affected by the --adc addition
    # ------------------------------------------------------------------
    def test_backward_compat_user_account(self):
        """-u alone → user_account=True, adc=False."""
        parser = self._parser()
        args = parser.parse_args(['gcp', '-u'])
        d = args.__dict__
        self.assertTrue(d.get('user_account'))
        self.assertFalse(d.get('adc', False))

    # ------------------------------------------------------------------
    # Verify -s (service account key file) still works exactly as before
    # and that adc remains False when a key file path is supplied
    # ------------------------------------------------------------------
    def test_backward_compat_service_account(self):
        """-s key.json alone → service_account='key.json', adc=False."""
        parser = self._parser()
        args = parser.parse_args(['gcp', '-s', 'key.json'])
        d = args.__dict__
        self.assertEqual(d.get('service_account'), 'key.json')
        self.assertFalse(d.get('adc', False))


if __name__ == '__main__':
    unittest.main()


# ---------------------------------------------------------------------------
# Property-based tests using Hypothesis
# ---------------------------------------------------------------------------
from hypothesis import given, settings
import hypothesis.strategies as st


class TestGCPAuthenticationStrategyProperties(unittest.TestCase):
    """Property-based tests for GCPAuthenticationStrategy using Hypothesis."""

    def _strategy(self):
        return GCPAuthenticationStrategy()

    # ------------------------------------------------------------------
    # Property 1: default_project_id attachment invariant
    #
    # For any non-empty project ID string and any of the three auth modes
    # (user_account, service_account, adc), authenticate() must always
    # attach default_project_id equal to the value returned by
    # google.auth.default(), regardless of what the project ID looks like.
    # ------------------------------------------------------------------
    @given(
        project_id=st.text(min_size=1),
        auth_mode=st.sampled_from([
            {'user_account': True},
            {'service_account': '/fake/key.json'},
            {'adc': True},
        ])
    )
    @settings(max_examples=100)
    def test_default_project_id_always_attached(self, project_id, auth_mode):
        """default_project_id is always attached to credentials, for any project ID and any auth mode."""
        mock_creds = MagicMock()

        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            return_value=(mock_creds, project_id)
        ), patch('os.path.abspath', return_value='/fake/key.json'), \
           patch.dict('os.environ', {}, clear=False):
            strategy = self._strategy()
            result = strategy.authenticate(**auth_mode)

        self.assertEqual(result.default_project_id, project_id)

    # ------------------------------------------------------------------
    # Property 2: Exception wrapping universality
    #
    # For any exception type raised by google.auth.default() during an
    # adc=True flow, authenticate() must always raise AuthenticationException
    # and never let the original exception type propagate to the caller.
    # ------------------------------------------------------------------
    @given(
        exc_type=st.sampled_from([
            ValueError,
            RuntimeError,
            OSError,
            Exception,
            __import__('google.auth.exceptions', fromlist=['DefaultCredentialsError']).DefaultCredentialsError,
        ])
    )
    @settings(max_examples=100)
    def test_all_exceptions_wrapped_as_authentication_exception(self, exc_type):
        """Any exception from google.auth.default() during adc=True is always wrapped as AuthenticationException."""
        with patch(
            'ScoutSuite.providers.gcp.authentication_strategy.auth.default',
            side_effect=exc_type('simulated failure')
        ):
            strategy = self._strategy()
            with self.assertRaises(AuthenticationException):
                strategy.authenticate(adc=True)
