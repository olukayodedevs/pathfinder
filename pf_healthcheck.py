#!/usr/bin/env python3

"""Endpoint Monitor"""

import requests, socket, time, csv, json
from datetime import datetime
import ssl, OpenSSL

# ===== Configs ===== #
ENDPOINTS = [
    "https://ac.pfgltd.com/testhealth",
    "https://secure.pfgltd.com/testhealth"
]
INTERVAL_SEC = 60
TOTAL_CHECKS = 60  # So there will be TOTAL_CHECKS checks at 60 seconds INTERVAL_SEC making it 1 hour total
OUTPUT_FILE = "pathfinder_health.csv"
# ================== #

def get_ips():
    """Get both IPs with failover"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            int_ip = s.getsockname()[0]
    except:
        int_ip = "N/A"
    
    try:
        ext_ip = requests.get("https://api.ipify.org", timeout=3).text
    except:
        ext_ip = "N/A"
    
    return int_ip, ext_ip

def get_endpoint_ip(url):
    """Resolve endpoint IP"""
    try:
        return socket.gethostbyname(url.split('/')[2])
    except:
        return "N/A"

def check_endpoint(url):
    """Full endpoint health check"""
    result = {
        'timestamp': datetime.utcnow().isoformat(),
        'endpoint_ip': get_endpoint_ip(url),
        'latency_ms': None,
        'status': 'ERROR',
        'cert_expiry': None,
        'error': None,
        'cpu_usage': None,
        'disk_usage': None,
        'memory_usage': None,
        'services': None
    }
    
    try:
        # measuring the latencies
        start = time.time()
        r = requests.get(url, timeout=5)
        result['latency_ms'] = round((time.time() - start) * 1000, 2)
        
        # SSL cert check
        host = url.split('/')[2]
        cert = ssl.get_server_certificate((host, 443))
        expiry = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert
        ).get_notAfter().decode('ascii')
        result['cert_expiry'] = f"{expiry[:4]}-{expiry[4:6]}-{expiry[6:8]}"
        
        # Parse JSON response
        data = r.json()
        result['status'] = data.get('status', 'UNKNOWN')
        result['cpu_usage'] = data.get('metrics', {}).get('cpu_usage')
        result['disk_usage'] = data.get('metrics', {}).get('disk_usage')
        result['memory_usage'] = data.get('metrics', {}).get('memory_usage')
        result['services'] = json.dumps(data.get('services', {}))
        
    except Exception as e:
        result['error'] = str(e)[:100]  # This is going to truncate long errors
    
    return result

###########################

def main():
    int_ip, ext_ip = get_ips()
    fieldnames = [
        'timestamp', 'internal_ip', 'external_ip', 'endpoint',
        'endpoint_ip', 'latency_ms', 'status', 'cert_expiry',
        'cpu_usage', 'disk_usage', 'memory_usage', 'services', 'error'
    ]
    
    with open(OUTPUT_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        
        for _ in range(TOTAL_CHECKS):
            cycle_start = time.time()
            
            for url in ENDPOINTS:
                data = check_endpoint(url)
                data.update({
                    'internal_ip': int_ip,
                    'external_ip': ext_ip,
                    'endpoint': url
                })
                writer.writerow(data)
                f.flush()
            
            elapsed = time.time() - cycle_start
            time.sleep(max(INTERVAL_SEC - elapsed, 0))

if __name__ == '__main__':
    main()
