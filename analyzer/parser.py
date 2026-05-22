import json
import re
from datetime import datetime, UTC

from .model import LogEntry


LOG_PATTERN = re.compile(
    r"""
    (?P<timestamp>\S+\s?\S*)
    \s+
    (?P<ip>\S+)
    \s+
    (?P<method>GET|POST|PUT|DELETE)
    \s+
    (?P<path>/\S*)
    (?:\s+(?P<status>\d{3}|-))?
    (?:\s+(?P<response>\S+))?
    $
    """,
    re.VERBOSE,
)


VALID_METHODS = {"GET", "POST", "PUT", "DELETE"}


def parse_timestamp(timestamp: str):

    if not timestamp:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y/%m/%d %H:%M:%S",
        "%d-%b-%Y %H:%M:%S",
    ]

    # Epoch timestamp
    if timestamp.isdigit():
        try:
            return datetime.fromtimestamp(
                int(timestamp),
                UTC,
            )
        except Exception:
            return None

    # Formatted timestamps
    for fmt in formats:
        try:
            return datetime.strptime(
                timestamp,
                fmt,
            )
        except ValueError:
            continue

    return None


def parse_response_time(value: str):

    if not value:
        return None

    value = value.strip()

    try:

        # milliseconds
        if value.endswith("ms"):
            return float(value[:-2])

        # seconds → convert to ms
        if value.endswith("s"):
            return float(value[:-1]) * 1000

        # plain number
        return float(value)

    except ValueError:
        return None


def parse_json_line(line: str):

    try:
        data = json.loads(line)

        return LogEntry(
            timestamp=parse_timestamp(
                str(data.get("timestamp"))
            ),
            ip=data.get("ip"),
            method=data.get("method"),
            path=data.get("path"),
            status=(
                int(data["status"])
                if data.get("status") is not None
                else None
            ),
            response_time_ms=parse_response_time(
                data.get("response_time")
            ),
            raw_line=line,
            malformed=False,
        )

    except Exception:
        return None


def parse_standard_line(line: str):

    match = LOG_PATTERN.fullmatch(line)

    if not match:
        return None

    data = match.groupdict()

    status = data.get("status")

    return LogEntry(
        timestamp=parse_timestamp(
            data.get("timestamp")
        ),
        ip=data.get("ip"),
        method=data.get("method"),
        path=data.get("path"),
        status=(
            int(status)
            if status and status != "-"
            else None
        ),
        response_time_ms=parse_response_time(
            data.get("response")
        ),
        raw_line=line,
        malformed=False,
    )


def build_malformed_entry(line: str):

    return LogEntry(
        timestamp=None,
        ip=None,
        method=None,
        path=None,
        status=None,
        response_time_ms=None,
        raw_line=line,
        malformed=True,
    )


def parse_line(line: str):

    line = line.strip()

    # Empty line
    if not line:
        return build_malformed_entry(line)

    # Try JSON parser
    entry = parse_json_line(line)

    # Try standard parser
    if not entry:
        entry = parse_standard_line(line)

    # Completely invalid line
    if not entry:
        return build_malformed_entry(line)

    # Validate method
    if entry.method not in VALID_METHODS:
        entry.malformed = True

    return entry