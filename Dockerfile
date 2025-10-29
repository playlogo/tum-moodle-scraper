FROM python:3.13-slim

# Prep os
RUN apt-get update && apt-get install -y \
    rsync \
    cron \
    && rm -rf /var/lib/apt/lists/*


# Prep for main
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium-headless-shell chromium
RUN playwright install-deps chromium-headless-shell chromium

RUN mkdir -p /usr/src/app/data

# Copy main
COPY src/ .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy cron job script
COPY run-moodle-scraper.sh /run-moodle-scraper.sh
RUN chmod +x /run-moodle-scraper.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["cron"]
