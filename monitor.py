import requests
import socket
import ssl
import urllib.parse
import time
from datetime import datetime

TARGETS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://httpbin.org/status/500",
    "https://domain-that-does-not-exist.com"
]

def get_ssl_expiry(url: str):
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname:
        return "N/A"
    
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                expire_date_str = cert['notAfter']
                expire_date = datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z")
                
                days_left = (expire_date - datetime.utcnow()).days
                return f"{days_left} days"
    except Exception:
        return "SSL Error/None"

def check_uptime(url: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ssl_status = get_ssl_expiry(url)
    
    try:
        response = requests.get(url, timeout=5)
        latency_ms = round(response.elapsed.total_seconds() * 1000, 2)
        
        if response.status_code == 200:
            log_msg = f"[{timestamp}] [ONLINE] {url} | Status: {response.status_code} | Latency: {latency_ms} ms | SSL: {ssl_status}"
        else:
            log_msg = f"[{timestamp}] [WARNING] {url} | Status: {response.status_code} | Latency: {latency_ms} ms | SSL: {ssl_status}"
            
    except requests.exceptions.RequestException as e:
        log_msg = f"[{timestamp}] [DOWN] {url} | SSL: {ssl_status} | ERROR: {e}"
    
    print(log_msg)
    
    with open("monitor.log", "a") as log_file:
        log_file.write(log_msg + "\n")

if __name__ == "__main__":
    print("Starting continuous uptime monitoring... (Press CTRL+C to stop)")
    
    while True:
        print(f"\n--- Running scan at {datetime.now().strftime('%H:%M:%S')} ---")
        for site in TARGETS:
            check_uptime(site)
            
        print("Scan complete. Waiting 60 seconds...")
        time.sleep(60)