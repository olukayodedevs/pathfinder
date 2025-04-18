#!/bin/bash
echo "=== Service Status ==="
sudo systemctl status pathfinder-monitor --no-pager | head -n 7

echo -e "\n=== Recent Logs ==="
sudo journalctl -u pathfinder-monitor -n 20 --no-pager

echo -e "\n=== CSV File ==="
sudo ls -lh /opt/pathfinder/pathfinder_health.csv
echo -e "\nLast 5 entries:"
sudo tail -n 5 /opt/pathfinder/pathfinder_health.csv
