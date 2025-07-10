import unittest
from unittest.mock import patch, MagicMock
from htping.headers import parse_headers
import io


class TestHeaders(unittest.TestCase):
    def test_parse_headers_valid(self):
        headers = [
            "Authorization: Bearer token",
            "Content-Type: application/json",
            "Accept: application/json",
        ]
        result = parse_headers(headers)
        expected = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.assertEqual(result, expected)

    def test_parse_headers_with_spaces(self):
        headers = [
            "  Authorization  :  Bearer token  ",
            "Content-Type:application/json",
        ]
        result = parse_headers(headers)
        expected = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }
        self.assertEqual(result, expected)

    def test_parse_headers_empty(self):
        result = parse_headers(None)
        self.assertEqual(result, {})

    def test_parse_headers_invalid_format(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            headers = ["invalid-header", "valid: header"]
            result = parse_headers(headers)
            
        output = mock_stdout.getvalue()
        self.assertIn("Invalid header format", output)
        self.assertEqual(result, {"valid": "header"})

    def test_parse_headers_multiple_colons(self):
        headers = ["Authorization: Bearer: token: with: colons"]
        result = parse_headers(headers)
        expected = {"Authorization": "Bearer: token: with: colons"}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()