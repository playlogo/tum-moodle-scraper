#!/bin/bash


# Run moodle-scraper
echo "$(date): Starting scheduled moodle-scraper run..."
cd /usr/src/app

/usr/local/bin/python main.py

echo "$(date): Scheduled moodle-scraper run completed"
