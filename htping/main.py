# htping/main.py

import requests
import httpx
import time
import sys
import signal
import argparse
import json
from typing import Optional, List, Dict, Any, Union

# Summary statistics  
stats: Dict[str, Any] = {"transmitted": 0, "received": 0, "rtt_times": []}


# Handler for SIGINT (Ctrl+C)
def signal_handler(sig: Any, frame: Any) -> None:
    print("\n--- htping statistics ---")
    transmitted = stats["transmitted"]
    received = stats["received"]
    packet_loss = (
        ((transmitted - received) / transmitted) * 100 if transmitted > 0 else 0
    )

    print(
        f"{transmitted} packets transmitted, {received} received, "
        f"{packet_loss:.0f}% packet loss"
    )

    if stats["rtt_times"]:
        min_rtt = min(stats["rtt_times"])
        avg_rtt = sum(stats["rtt_times"]) / len(stats["rtt_times"])
        max_rtt = max(stats["rtt_times"])
        print(f"rtt min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")

    sys.exit(0)


# Setup signal handler
signal.signal(signal.SIGINT, signal_handler)


def htping(
    url: str,
    interval: float,
    count: Optional[int] = None,
    method: str = "GET",
    timeout: float = 10.0,
    headers: Optional[List[str]] = None,
    data: Optional[str] = None,
    follow_redirects: bool = True,
    max_redirects: int = 5,
    http2: bool = False,
) -> None:
    """Send HTTP requests to a URL at regular intervals.

    Args:
        url: The target URL to ping
        interval: Time in seconds between requests
        count: Optional limit on number of requests
        method: HTTP method to use
        timeout: Request timeout in seconds
        headers: List of custom headers in "Name: Value" format
        data: Request body data
        follow_redirects: Whether to follow redirects
        max_redirects: Maximum number of redirects to follow
        http2: Whether to force HTTP/2 usage
    """
    # Parse and validate headers
    parsed_headers = {}
    if headers:
        for header in headers:
            if ":" not in header:
                print(
                    f"Warning: Invalid header format '{header}'. "
                    f"Expected 'Name: Value'"
                )
                continue
            name, value = header.split(":", 1)
            parsed_headers[name.strip()] = value.strip()

    # Auto-detect JSON data and set Content-Type
    if data:
        try:
            json.loads(data)
            if (
                "Content-Type" not in parsed_headers
                and "content-type" not in parsed_headers
            ):
                parsed_headers["Content-Type"] = "application/json"
        except json.JSONDecodeError:
            pass  # Not JSON, leave as is

    # Validate HTTP method
    method = method.upper()
    if method not in ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]:
        print(f"Error: Unsupported HTTP method '{method}'")
        sys.exit(1)

    # Choose HTTP client based on http2 flag
    if http2:
        client = httpx.Client(
            timeout=timeout,
            follow_redirects=follow_redirects,
            max_redirects=max_redirects,
            http2=True,
        )
    else:
        # Use requests for HTTP/1.1
        session = requests.Session()
        if not follow_redirects:
            session.max_redirects = 0
        else:
            session.max_redirects = max_redirects

    seq = 0
    try:
        while count is None or seq < count:
            seq += 1
            stats["transmitted"] += 1
            start_time = time.time()

            try:
                response: Union[httpx.Response, requests.Response]
                if http2:
                    # Use httpx for HTTP/2
                    response = client.request(
                        method=method,
                        url=url,
                        headers=parsed_headers,
                        content=data,
                    )
                    elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                    size = len(response.content)
                    status = response.status_code
                    protocol = f"HTTP/{response.http_version}"
                else:
                    # Use requests for HTTP/1.1
                    response = session.request(
                        method=method,
                        url=url,
                        headers=parsed_headers,
                        data=data,
                        timeout=timeout,
                        allow_redirects=follow_redirects,
                    )
                    elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                    size = len(response.content) if method != "HEAD" else 0
                    status = response.status_code
                    protocol = "HTTP/1.1"

                # Format output with additional info
                output_parts = [
                    f"{size} bytes from {url}",
                    f"http_seq={seq}",
                    f"status={status}",
                    f"time={elapsed_time:.2f} ms",
                ]

                if http2:
                    output_parts.append(f"protocol={protocol}")

                # Add redirect info if redirects occurred
                if hasattr(response, "history") and response.history:
                    output_parts.append(f"redirects={len(response.history)}")

                print(" ".join(output_parts))

                stats["received"] += 1
                stats["rtt_times"].append(elapsed_time)

            except requests.exceptions.Timeout:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(f"Request timeout: http_seq={seq} time={elapsed_time:.2f} ms")
            except requests.exceptions.TooManyRedirects:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(f"Too many redirects: http_seq={seq} time={elapsed_time:.2f} ms")
            except (requests.RequestException, httpx.RequestError) as e:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(
                    f"Request failed: http_seq={seq} time={elapsed_time:.2f} ms - {e}"
                )
            except Exception as e:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(
                    f"Unexpected error: http_seq={seq} time={elapsed_time:.2f} ms - {e}"
                )

            time.sleep(interval)

    finally:
        if http2:
            client.close()


def main() -> None:
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

    htping(
        args.url,
        args.interval,
        args.count,
        method=args.method,
        timeout=args.timeout,
        headers=args.header,
        data=args.data,
        follow_redirects=not args.no_follow_redirects,
        max_redirects=args.max_redirects,
        http2=args.http2,
    )
