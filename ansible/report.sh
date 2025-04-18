#!/bin/bash

CSV_PATH="/opt/pathfinder/pathfinder_health.csv"
SCRIPT_PATH="$(dirname "$0")/pf_analyze.py"



echo "Generating Pathfinder report..."

# this will check if the CSV exists
if [ ! -f "$CSV_PATH" ]; then
    echo "Health check CSV not found at $CSV_PATH"
    echo "Make sure the monitoring service has generated some data."
    exit 1
fi

# checks if  analysis script exists

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Analysis script not found at $SCRIPT_PATH"
    exit 1
fi

# Run the analysis
python3 "$SCRIPT_PATH"

