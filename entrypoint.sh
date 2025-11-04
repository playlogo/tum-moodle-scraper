#!/bin/bash
set -e

# Set default interval if not provided
INTERVAL_HOURS=${RUN_INTERVAL_HOURS:-24h}

echo "DEBUG $(date): Python location:"
echo $(which python)

echo "$(date): Starting loop "
while true
do
    echo "$(date): Running moodle scraper..."
    cd /usr/src/app
    /usr/local/bin/python main.py
    echo "$(date): moodle scraper completed"
    sleep $INTERVAL_HOURS
done
