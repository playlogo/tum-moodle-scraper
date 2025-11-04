FROM python:3.13-slim

# Prep os
RUN apt-get update && apt-get install -y rsync && rm -rf /var/lib/apt/lists/*

# Prep for main
WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/data
COPY requirements.txt ./
COPY entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium-headless-shell
RUN playwright install-deps chromium-headless-shell

# Copy main
COPY src/ .

# Copy entrypoint script
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
