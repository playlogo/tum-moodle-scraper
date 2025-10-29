#!/bin/bash

# Change to downloads directory
cd /usr/src/app

# Run moodle-scraper
echo "$(date): Starting scheduled moodle-scraper run..."
python main.py
echo "$(date): Scheduled moodle-scraper run completed"
