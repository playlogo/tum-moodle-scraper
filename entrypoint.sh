#!/bin/bash
set -e

# Set default interval if not provided
INTERVAL_HOURS=${RUN_INTERVAL_HOURS:-12}

run_moodle_scraper() {
    echo "$(date): Running moodle scraper..."
    cd /usr/src/app
    python main.py
    echo "$(date): moodle scraper completed"
}

if [ "$1" = "run-once" ]; then
    echo "Running moodle scraper once..."
    run_moodle_scraper
    exit 0
fi

# Setup cron job
if [ "$1" = "cron" ]; then
    echo "Setting up cron job to run every ${INTERVAL_HOURS} hours..."
    
    # Calculate cron schedule
    # For simplicity, we'll use a script that runs every hour and checks if it should execute
    echo "0 */${INTERVAL_HOURS} * * * /run-moodle-scraper.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/moodle-scraper-cron
    
    # Give execution rights on the cron job
    chmod 0644 /etc/cron.d/moodle-scraper-cron
    
    # Apply cron job
    crontab /etc/cron.d/moodle-scraper-cron
    
    # Create log file
    touch /var/log/cron.log
    
    # Run once immediately
    run_moodle_scraper
    
    # Start cron in foreground
    echo "Starting cron daemon..."
    cron && tail -f /var/log/cron.log
fi

# If no recognized command, pass through
exec "$@"
