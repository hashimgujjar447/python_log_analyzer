from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    timestamp: datetime | None
    ip: str | None
    method: str | None
    path: str | None
    status: int | None
    response_time_ms: float | None
    raw_line: str
    malformed: bool = False