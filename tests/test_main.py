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

    @patch("htping.main.requests.get")
    def test_htping_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"foo": "bar"}'
        mock_get.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            htping("http://example.com", 0.1, 1)  # Run htping for 1 iteration

        self.assertEqual(stats["transmitted"], 1)
        self.assertEqual(stats["received"], 1)
        self.assertEqual(len(stats["rtt_times"]), 1)
        self.assertGreater(stats["rtt_times"][0], 0)

    @patch("htping.main.requests.get")
    def test_htping_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
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


if __name__ == "__main__":
    unittest.main()
