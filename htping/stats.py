# htping/stats.py

import sys
import signal
from typing import Dict, Any


# Summary statistics
stats: Dict[str, Any] = {"transmitted": 0, "received": 0, "rtt_times": []}


def signal_handler(sig: Any, frame: Any) -> None:
    """Handler for SIGINT (Ctrl+C) to display statistics."""
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


def setup_signal_handler() -> None:
    """Setup signal handler for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)
