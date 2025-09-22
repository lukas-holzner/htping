import io
import signal as signal_module
import unittest
from unittest.mock import patch

from htping.stats import setup_signal_handler, signal_handler, stats


class TestStats(unittest.TestCase):
    def setUp(self):
        stats["transmitted"] = 0
        stats["received"] = 0
        stats["rtt_times"] = []

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_signal_handler_with_stats(self, mock_stdout):
        stats["transmitted"] = 10
        stats["received"] = 8
        stats["rtt_times"] = [1.0, 2.0, 3.0]

        with self.assertRaises(SystemExit):
            signal_handler(None, None)

        output = mock_stdout.getvalue()
        self.assertIn("10 packets transmitted", output)
        self.assertIn("8 received", output)
        self.assertIn("20% packet loss", output)
        self.assertIn("rtt min/avg/max = 1.000/2.000/3.000 ms", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_signal_handler_no_stats(self, mock_stdout):
        stats["transmitted"] = 0
        stats["received"] = 0
        stats["rtt_times"] = []

        with self.assertRaises(SystemExit):
            signal_handler(None, None)

        output = mock_stdout.getvalue()
        self.assertIn("0 packets transmitted", output)
        self.assertIn("0 received", output)
        self.assertIn("0% packet loss", output)
        self.assertNotIn("rtt min/avg/max", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_signal_handler_perfect_success(self, mock_stdout):
        stats["transmitted"] = 5
        stats["received"] = 5
        stats["rtt_times"] = [10.0, 20.0, 30.0, 40.0, 50.0]

        with self.assertRaises(SystemExit):
            signal_handler(None, None)

        output = mock_stdout.getvalue()
        self.assertIn("5 packets transmitted", output)
        self.assertIn("5 received", output)
        self.assertIn("0% packet loss", output)
        self.assertIn("rtt min/avg/max = 10.000/30.000/50.000 ms", output)

    @patch("signal.signal")
    def test_setup_signal_handler(self, mock_signal):
        setup_signal_handler()
        mock_signal.assert_called_once_with(signal_module.SIGINT, signal_handler)


if __name__ == "__main__":
    unittest.main()
