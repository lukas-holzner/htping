import unittest
from htping.main import htping, stats, signal_handler
from unittest.mock import patch, MagicMock
import requests
import io


class TestHtping(unittest.TestCase):
    def setUp(self):
        stats["transmitted"] = 0
        stats["received"] = 0
        stats["rtt_times"] = []

    @patch("htping.main.requests.Session.request")
    def test_htping_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"foo": "bar"}'
        mock_response.history = []
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1)  # Run htping for 1 iteration

        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)
        self.assertEqual(len(stats["rtt_times"]), 1)
        self.assertGreater(stats["rtt_times"][0], 0)

    @patch("htping.main.requests.Session.request")
    def test_htping_failure(self, mock_request):
        mock_request.side_effect = requests.RequestException

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1)  # Run htping for 1 iteration

        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 0)
        self.assertEqual(len(stats["rtt_times"]), 0)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_signal_handler(self, mock_stdout):
        stats["transmitted"] = 10
        stats["received"] = 8
        stats["rtt_times"] = [1.0, 2.0, 3.0]

        with self.assertRaises(SystemExit):
            signal_handler(None, None)

        output = mock_stdout.getvalue()
        self.assertIn("10 packets transmitted", output)
        self.assertIn("8 received", output)
        self.assertIn("20% packet loss", output)
        self.assertIn("rtt min/avg/max", output)

    # Test new features
    @patch("htping.main.requests.Session.request")
    def test_htping_post_method(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.history = []
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1, method="POST")

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["method"], "POST")
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)

    @patch("htping.main.requests.Session.request")
    def test_htping_custom_headers(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.history = []
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping(
                "http://example.com",
                0.1,
                1,
                headers=[
                    "Authorization: Bearer token",
                    "Content-Type: application/json",
                ],
            )

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["headers"]["Authorization"], "Bearer token")
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("htping.main.requests.Session.request")
    def test_htping_json_data(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.history = []
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1, data='{"key": "value"}')

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["data"], '{"key": "value"}')
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("htping.main.requests.Session.request")
    def test_htping_timeout(self, mock_request):
        mock_request.side_effect = requests.exceptions.Timeout

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, timeout=5.0)

        output = mock_stdout.getvalue()
        self.assertIn("Request timeout", output)
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 0)

    @patch("htping.main.requests.Session.request")
    def test_htping_too_many_redirects(self, mock_request):
        mock_request.side_effect = requests.exceptions.TooManyRedirects

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1)

        output = mock_stdout.getvalue()
        self.assertIn("Too many redirects", output)
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 0)

    @patch("htping.main.requests.Session.request")
    def test_htping_head_method(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Some content"
        mock_response.history = []
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, method="HEAD")

        output = mock_stdout.getvalue()
        self.assertIn("0 bytes from", output)  # HEAD should show 0 bytes
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)

    @patch("htping.main.httpx.Client")
    def test_htping_http2(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "2.0"
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, http2=True)

        output = mock_stdout.getvalue()
        self.assertIn("protocol=HTTP/2.0", output)
        mock_client.request.assert_called_once()
        mock_client.close.assert_called_once()
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)

    @patch("htping.main.requests.Session.request")
    def test_htping_redirects_info(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.history = [MagicMock(), MagicMock()]  # 2 redirects
        mock_request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1)

        output = mock_stdout.getvalue()
        self.assertIn("redirects=2", output)
        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)

    def test_invalid_http_method(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit):
                htping("http://example.com", 0.1, 1, method="INVALID")

        output = mock_stdout.getvalue()
        self.assertIn("Unsupported HTTP method", output)

    def test_invalid_header_format(self):
        with patch("htping.main.requests.Session.request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b'{"success": true}'
            mock_response.history = []
            mock_request.return_value = mock_response

            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                htping("http://example.com", 0.1, 1, headers=["invalid-header"])

            output = mock_stdout.getvalue()
            self.assertIn("Invalid header format", output)


if __name__ == "__main__":
    unittest.main()
