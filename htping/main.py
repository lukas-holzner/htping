# htping/main.py

import requests
import time
import sys
import signal
import argparse

# Summary statistics
stats = {"transmitted": 0, "received": 0, "rtt_times": []}


# Handler for SIGINT (Ctrl+C)
def signal_handler(sig, frame):
    print("\n--- htping statistics ---")
    transmitted = stats["transmitted"]
    received = stats["received"]
    packet_loss = (
        ((transmitted - received) / transmitted) * 100 if transmitted > 0 else 0
    )

    print(
        f"{transmitted} packets transmitted, {received} received, {packet_loss:.0f}% packet loss"
    )

    if stats["rtt_times"]:
        min_rtt = min(stats["rtt_times"])
        avg_rtt = sum(stats["rtt_times"]) / len(stats["rtt_times"])
        max_rtt = max(stats["rtt_times"])
        print(f"rtt min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")

    sys.exit(0)


# Setup signal handler
signal.signal(signal.SIGINT, signal_handler)


def htping(url, interval, count=None):
    seq = 0
    while count is None or seq < count:
        seq += 1
        stats["transmitted"] += 1
        start_time = time.time()

        try:
            response = requests.get(url)
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            size = len(response.content)
            status = response.status_code

            print(
                f"{size} bytes from {url}: http_seq={seq} status={status} time={elapsed_time:.2f} ms"
            )

            stats["received"] += 1
            stats["rtt_times"].append(elapsed_time)

        except requests.RequestException as e:
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            print(f"Request failed: http_seq={seq} time={elapsed_time:.2f} ms")

        time.sleep(interval)


def main():
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
    args = parser.parse_args()

    htping(args.url, args.interval, args.count)
