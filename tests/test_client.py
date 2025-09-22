import io
import unittest
from unittest.mock import MagicMock, patch

import httpx

from htping.client import htping


class TestClient(unittest.TestCase):
    def setUp(self):
        self.stats = {"transmitted": 0, "received": 0, "rtt_times": []}

    @patch("htping.client.httpx.Client")
    def test_htping_success(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"foo": "bar"}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1, stats=self.stats)

        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)
        self.assertEqual(len(self.stats["rtt_times"]), 1)
        self.assertGreater(self.stats["rtt_times"][0], 0)
        mock_client.close.assert_called_once()

    @patch("htping.client.httpx.Client")
    def test_htping_failure(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.RequestError("Connection failed")

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1, stats=self.stats)

        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)
        self.assertEqual(len(self.stats["rtt_times"]), 0)
        mock_client.close.assert_called_once()

    @patch("htping.client.httpx.Client")
    def test_htping_post_method(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping("http://example.com", 0.1, 1, method="POST", stats=self.stats)

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["method"], "POST")
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("htping.client.httpx.Client")
    def test_htping_custom_headers(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping(
                "http://example.com",
                0.1,
                1,
                headers=[
                    "Authorization: Bearer token",
                    "Content-Type: application/json",
                ],
                stats=self.stats,
            )

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["headers"]["Authorization"], "Bearer token")
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("htping.client.httpx.Client")
    def test_htping_json_data(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            htping(
                "http://example.com", 0.1, 1, data='{"key": "value"}', stats=self.stats
            )

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["content"], '{"key": "value"}')
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("htping.client.httpx.Client")
    def test_htping_timeout(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.TimeoutException("Request timeout")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, timeout=5.0, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("Request timeout", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)

    @patch("htping.client.httpx.Client")
    def test_htping_too_many_redirects(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.TooManyRedirects("Too many redirects")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("Too many redirects", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)

    @patch("htping.client.httpx.Client")
    def test_htping_head_method(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Some content"
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, method="HEAD", stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("0 bytes from", output)  # HEAD should show 0 bytes
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("htping.client.httpx.Client")
    def test_htping_http2(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "2.0"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, http2=True, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("protocol=HTTP/2.0", output)

        # Check that client was created with http2=True
        mock_client_class.assert_called_once()
        call_args = mock_client_class.call_args
        self.assertTrue(call_args[1]["http2"])

        mock_client.request.assert_called_once()
        mock_client.close.assert_called_once()
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("htping.client.httpx.Client")
    def test_htping_redirects_info(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = [MagicMock(), MagicMock()]  # 2 redirects
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("redirects=2", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    def test_invalid_http_method(self):
        with self.assertRaises(ValueError) as context:
            htping("http://example.com", 0.1, 1, method="INVALID", stats=self.stats)

        self.assertIn("Unsupported HTTP method", str(context.exception))

    @patch("htping.client.httpx.Client")
    def test_invalid_header_format(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping(
                "http://example.com",
                0.1,
                1,
                headers=["invalid-header"],
                stats=self.stats,
            )

        output = mock_stdout.getvalue()
        self.assertIn("Invalid header format", output)


if __name__ == "__main__":
    unittest.main()
