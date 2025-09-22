# hping/client.py

import json
import time
from typing import Any, Dict, List, Optional

import httpx


def hping(
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
    stats: Optional[Dict[str, Any]] = None,
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
        stats: Statistics dictionary to update
    """
    from .headers import parse_headers

    if stats is None:
        stats = {"transmitted": 0, "received": 0, "rtt_times": []}

    # Parse and validate headers
    parsed_headers = parse_headers(headers)

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
        raise ValueError(f"Unsupported HTTP method '{method}'")

    # Create httpx client with appropriate settings
    client = httpx.Client(
        timeout=timeout,
        follow_redirects=follow_redirects,
        max_redirects=max_redirects,
        http2=http2,
    )

    seq = 0
    try:
        while count is None or seq < count:
            seq += 1
            stats["transmitted"] += 1
            start_time = time.time()

            try:
                response = client.request(
                    method=method,
                    url=url,
                    headers=parsed_headers,
                    content=data,
                )
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                size = len(response.content) if method != "HEAD" else 0
                status = response.status_code
                protocol = f"HTTP/{response.http_version}"

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

            except httpx.TimeoutException:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(f"Request timeout: http_seq={seq} time={elapsed_time:.2f} ms")
            except httpx.TooManyRedirects:
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
                print(f"Too many redirects: http_seq={seq} time={elapsed_time:.2f} ms")
            except httpx.RequestError as e:
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
        client.close()
