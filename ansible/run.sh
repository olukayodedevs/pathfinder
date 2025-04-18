#!/bin/bash
#
echo "installing ansible>>>"
sudo apt update && sudo apt install -y ansible

echo "Starting deployment..."
sudo ansible-playbook -i inventory.ini deploy.yml
if [ $? -eq 0 ]; then
    echo "Deployment successful!"
    echo "CSV will be created at: /opt/pathfinder/pathfinder_health.csv"
    echo "Run: sudo tail -f /opt/pathfinder/pathfinder_health.csv"
else
    echo "Deployment failed!"
    exit 1
fi
