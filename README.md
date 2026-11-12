# Uptime & SSL Security Monitor

A continuous background worker script built with Python to monitor website uptime, HTTP response latency, and SSL certificate expiration dates.

## Features
- **HTTP Uptime Monitoring:** Checks server status codes (200, 500, etc.) and measures network latency in milliseconds.
- **SSL Certificate Audit:** Extracts and calculates the remaining valid days for HTTPS certificates directly via low-level sockets.
- **Automated Logging:** Saves all monitoring history permanently to `monitor.log`.
- **Infinite Execution:** Runs continuously as a background worker with configurable delay intervals.

## Technology Stack
- Python 3
- `requests` (HTTP Client)
- `socket` & `ssl` (Low-level networking & security)

## How to Run
1. Clone this repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate