from unittest import TestCase

from mock import MagicMock, patch

from ScoutSuite.__main__ import main
from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser


class TestMainClass(TestCase):

    def setUp(self):
        self.constructor = {}
        self.mocked_provider = MagicMock()

        self.mocked_engine = MagicMock()
        self.mocked_report = MagicMock()
        self.mocked_browser = MagicMock()
        self.mocked_ruleset = MagicMock()

        self.mocked_printInfo = MagicMock()

        for import_name, mocked_object in [("print_info", self.mocked_printInfo),
                                           ("get_provider", self.mocked_provider),
                                           ("Ruleset", self.mocked_ruleset),
                                           ("ProcessingEngine", self.mocked_engine),
                                           ("Scout2Report", self.mocked_report),
                                           ("webbrowser", self.mocked_browser)]:
            constructor_obj = patch("ScoutSuite.__main__.%s" % import_name, return_value=mocked_object).start()
            self.constructor[mocked_object] = constructor_obj

        self.mocked_report.save = MagicMock(return_value="dummyfile")

    def tearDown(self):
        patch.stopall()

    def test_empty(self):
        args = None
        code = None

        with patch("sys.stderr", return_value=MagicMock()):
            with self.assertRaises(SystemExit):
                args = ScoutSuiteArgumentParser().parse_args(args)
                code = main(args)

        assert (code is None)

    def test_aws_provider(self):
        args = ['aws']
        self.mocked_provider.provider_code = "aws"

        args = ScoutSuiteArgumentParser().parse_args(args)
        code = main(args)

        success_code = 0
        assert (code == success_code)

        report_init_args = self.constructor[self.mocked_report].call_args_list[0][0]
        assert (report_init_args[0] == "aws")  # provider
        assert (report_init_args[1] == "aws-default")  # report_file_name
        assert (report_init_args[2] == "scoutsuite-report")  # report_dir

    def test_gcp_provider(self):
        args = ["gcp", "--service-account", "fakecredentials"]
        self.mocked_provider.provider_code = "gcp"

        args = ScoutSuiteArgumentParser().parse_args(args)
        code = main(args)

        success_code = 0
        assert (code == success_code)

        report_init_args = self.constructor[self.mocked_report].call_args_list[0][0]
        assert (report_init_args[0] == "gcp")  # provider
        assert (report_init_args[1] == "gcp")  # report_file_name
        assert (report_init_args[2] == "scoutsuite-report")  # report_dir

    def test_azure_provider(self):
        args = ["azure", "--cli"]
        self.mocked_provider.provider_code = "azure"

        args = ScoutSuiteArgumentParser().parse_args(args)
        code = main(args)

        success_code = 0
        assert (code == success_code)

        report_init_args = self.constructor[self.mocked_report].call_args_list[0][0]
        assert (report_init_args[0] == "azure")  # provider
        assert (report_init_args[1] == "azure")  # report_file_name
        assert (report_init_args[2] == "scoutsuite-report")  # report_dir

    def test_unauthenticated(self):
        args = ["aws"]
        self.mocked_provider.provider_code = "aws"
        self.mocked_provider.authenticate = MagicMock(return_value=False)

        args = ScoutSuiteArgumentParser().parse_args(args)
        code = main(args)

        unauthenticated_code = 42
        assert (code == unauthenticated_code)

    def test_keyboardinterrupted(self):
        args = ["aws"]
        self.mocked_provider.provider_code = "aws"

        def _raise(e):
            raise e

        self.mocked_provider.fetch = MagicMock(side_effect=_raise(KeyboardInterrupt))

        args = ScoutSuiteArgumentParser().parse_args(args)
        code = main(args)

        keyboardinterrupted_code = 130
        assert (code == keyboardinterrupted_code)
