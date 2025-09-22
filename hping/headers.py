# hping/headers.py

from typing import Dict, List, Optional


def parse_headers(headers: Optional[List[str]]) -> Dict[str, str]:
    """Parse and validate headers from command line format.

    Args:
        headers: List of headers in "Name: Value" format

    Returns:
        Dictionary of parsed headers
    """
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

    return parsed_headers
