FROM python:3.13-slim

# Create lower privilege user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid 1000 --create-home appuser

# Install rsync
RUN apt-get update && apt-get install --no-install-recommends -y rsync && rm -rf /var/lib/apt/lists/*

# Prep for main
WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/data
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install-deps chromium-headless-shell && rm -rf /var/lib/apt/lists/*

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Permissions
RUN chown -R appuser:appgroup /usr/src/app
RUN chown appuser:appgroup /entrypoint.sh

USER 1000

RUN playwright install chromium-headless-shell

# Copy main
COPY src/ .

ENTRYPOINT ["/entrypoint.sh"]
