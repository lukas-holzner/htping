# hping/main.py

import argparse
import sys

from .client import hping
from .stats import setup_signal_handler, stats


def main() -> None:
    """Main CLI entry point."""
    setup_signal_handler()

    parser = argparse.ArgumentParser(description="HTTP Ping CLI Tool")
    parser.add_argument("url", type=str, help="URL to ping")
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1.0,
        help="Interval in seconds between requests",
    )
    parser.add_argument(
        "-c", "--count", type=int, default=None, help="Number of pings to send"
    )

    # HTTP Method
    parser.add_argument(
        "-X",
        "--method",
        type=str,
        default="GET",
        help="HTTP method to use (GET, POST, PUT, DELETE, HEAD, PATCH). Default: GET",
    )

    # Timeout
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Request timeout in seconds. Default: 10.0",
    )

    # Custom Headers
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        default=[],
        help="Custom HTTP header in format 'Name: Value'. Can be used multiple times",
    )

    # Request Body
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="Request body data. Auto-detects JSON format",
    )

    # Redirect Control
    parser.add_argument(
        "--no-follow-redirects",
        action="store_true",
        help="Disable redirect following",
    )

    parser.add_argument(
        "--max-redirects",
        type=int,
        default=5,
        help="Maximum number of redirects to follow. Default: 5",
    )

    # HTTP/2 Support
    parser.add_argument(
        "--http2",
        action="store_true",
        help="Force HTTP/2 usage",
    )

    args = parser.parse_args()

    # Validate HTTP method
    method = args.method.upper()
    if method not in ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]:
        print(f"Error: Unsupported HTTP method '{method}'")
        sys.exit(1)

    hping(
        args.url,
        args.interval,
        args.count,
        method=method,
        timeout=args.timeout,
        headers=args.header,
        data=args.data,
        follow_redirects=not args.no_follow_redirects,
        max_redirects=args.max_redirects,
        http2=args.http2,
        stats=stats,
    )
