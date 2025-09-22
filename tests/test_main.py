import io
import sys
import unittest
from unittest.mock import patch

from hping.main import main


class TestMain(unittest.TestCase):
    @patch("hping.main.hping")
    @patch("hping.main.setup_signal_handler")
    def test_main_basic_args(self, mock_setup, mock_hping):
        test_args = ["hping", "http://example.com"]

        with patch.object(sys, "argv", test_args):
            main()

        mock_setup.assert_called_once()
        mock_hping.assert_called_once()
        call_args = mock_hping.call_args
        self.assertEqual(call_args[0][0], "http://example.com")  # url
        self.assertEqual(call_args[0][1], 1.0)  # interval
        self.assertEqual(call_args[0][2], None)  # count
        self.assertEqual(call_args[1]["method"], "GET")
        self.assertEqual(call_args[1]["timeout"], 10.0)
        self.assertEqual(call_args[1]["headers"], [])
        self.assertEqual(call_args[1]["data"], None)
        self.assertEqual(call_args[1]["follow_redirects"], True)
        self.assertEqual(call_args[1]["max_redirects"], 5)
        self.assertEqual(call_args[1]["http2"], False)

    @patch("hping.main.hping")
    @patch("hping.main.setup_signal_handler")
    def test_main_with_options(self, mock_setup, mock_hping):
        test_args = [
            "hping",
            "http://example.com",
            "-X",
            "POST",
            "-i",
            "2.0",
            "-c",
            "5",
            "--timeout",
            "30",
            "-H",
            "Authorization: Bearer token",
            "-H",
            "Content-Type: application/json",
            "-d",
            '{"key": "value"}',
            "--no-follow-redirects",
            "--max-redirects",
            "10",
            "--http2",
        ]

        with patch.object(sys, "argv", test_args):
            main()

        mock_setup.assert_called_once()
        mock_hping.assert_called_once()
        call_args = mock_hping.call_args
        self.assertEqual(call_args[0][0], "http://example.com")  # url
        self.assertEqual(call_args[0][1], 2.0)  # interval
        self.assertEqual(call_args[0][2], 5)  # count
        self.assertEqual(call_args[1]["method"], "POST")
        self.assertEqual(call_args[1]["timeout"], 30.0)
        self.assertEqual(
            call_args[1]["headers"],
            ["Authorization: Bearer token", "Content-Type: application/json"],
        )
        self.assertEqual(call_args[1]["data"], '{"key": "value"}')
        self.assertEqual(call_args[1]["follow_redirects"], False)
        self.assertEqual(call_args[1]["max_redirects"], 10)
        self.assertEqual(call_args[1]["http2"], True)

    @patch("hping.main.hping")
    @patch("hping.main.setup_signal_handler")
    def test_main_invalid_method(self, mock_setup, mock_hping):
        test_args = ["hping", "http://example.com", "-X", "INVALID"]

        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                with self.assertRaises(SystemExit):
                    main()

        output = mock_stdout.getvalue()
        self.assertIn("Unsupported HTTP method", output)
        mock_setup.assert_called_once()
        mock_hping.assert_not_called()

    @patch("hping.main.hping")
    @patch("hping.main.setup_signal_handler")
    def test_main_case_insensitive_method(self, mock_setup, mock_hping):
        test_args = ["hping", "http://example.com", "-X", "post"]

        with patch.object(sys, "argv", test_args):
            main()

        mock_setup.assert_called_once()
        mock_hping.assert_called_once()
        call_args = mock_hping.call_args
        self.assertEqual(call_args[1]["method"], "POST")


if __name__ == "__main__":
    unittest.main()
