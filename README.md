# Log Analyzer

A fault-tolerant log analyzer built in Python.

This tool parses mixed-format server logs and generates useful analytics while gracefully handling malformed lines and inconsistent log formats.

## Features

- Parses standard log lines
- Supports multiple timestamp formats
- Supports JSON-formatted log entries
- Handles malformed lines safely
- Supports mixed response time units
- Generates endpoint and status code analytics
- Detects slow endpoints

## Supported Log Variations

- ISO timestamps
- Slash timestamps
- Apache-style timestamps
- Unix epoch timestamps
- JSON logs
- Missing fields
- Malformed lines
- Stack traces

---

# Setup

## Install dependencies

Python 3.11+ is required.
---

# Generate Sample Logs

```bash
python scripts/generate_logs.py
```

This creates:

```txt
sample_logs/generated_logs.log
```

---

# Run Analyzer

```bash
python main.py sample_logs/generated_logs.log
```

---

# Example Output

```txt
===== LOG ANALYSIS =====

Parsed lines: 7997
Malformed lines: 2913

Status code counts:
Counter({200: 2102, 404: 812})

Endpoint counts:
Counter({'/api/users': 921})

Average response time: 488.22 ms

Top 5 slowest endpoints:
/api/search -> 921 ms
```

---

# Project Structure

```txt
log-analyzer/
│
├── analyzer/
│   ├── model.py
│   ├── parser.py
│   └── stats.py
│
├── sample_logs/
│
├── scripts/
│   └── generate_logs.py
│
├── main.py
├── README.md
├── ANSWERS.md
└── requirements.txt
```

---

# Design Notes

The parser is intentionally fault-tolerant.

Malformed or unexpected lines do not crash the application. Instead, they are marked as malformed and excluded from analytics while still being counted in the final report.