#!/usr/bin/env python3
""" Health Report"""

import pandas as pd

def to_float(series):
    """Convert '34.5%' strings to float 34.5 safely"""
    return pd.to_numeric(series.astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')

def analyze():
    df = pd.read_csv("pathfinder_health.csv")
    
    print("=== Pathfinder SLA Report ===")
    for endpoint in df.endpoint.unique():
        subset = df[df.endpoint == endpoint]
        total = subset.shape[0]
        up_subset = subset[subset.status == 'success']
        up_count = up_subset.shape[0]

        uptime = (up_count / total) * 100 if total else 0
        avg_latency = pd.to_numeric(subset.latency_ms, errors='coerce').mean()
        avg_response_time = pd.to_numeric(up_subset.latency_ms, errors='coerce').mean()

        avg_cpu = to_float(subset["cpu_usage"]).mean()
        avg_disk = to_float(subset["disk_usage"]).mean()
        avg_memory = to_float(subset["memory_usage"]).mean()

        cert_expiry = subset.cert_expiry.dropna().iloc[0] if not subset.cert_expiry.dropna().empty else "N/A"

        print(f"\n {endpoint}")
        print(f" Uptime: {uptime:.2f}%")
        print(f" Avg Latency (All): {avg_latency:.2f} ms")
        print(f" Avg Response Time (When UP): {avg_response_time:.2f} ms")
        print(f" Cert Expires: {cert_expiry}")
        print(f" Avg CPU: {avg_cpu:.2f}%")
        print(f" Avg Disk: {avg_disk:.2f}%")
        print(f" Avg Memory: {avg_memory:.2f}%")

        if uptime < 99.9:
            print("  Below 99.9% SLA")

if __name__ == '__main__':
    analyze()
