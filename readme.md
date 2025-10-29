# TUM Moodle scraper

Automatically regularly scrape your TUM Moodle to download all files.
Useful if combined with (for example) Syncthing, to automatically download the lecture slides & exercise sheets to your laptop & tablet.

Bundled into a docker container (docker compose included) to allow easy setup - See [Getting started](#getting-started)

## Getting started

1. Clone this repo (ideally to a server running 24/7): `git clone https://github.com/playlogo/tum-moodle-scraper && cd tum-moodle-scraper`
2. Create a `.env` file with your TUM shibboleth login credentials:

```env
USERNAME=<your username>
PASSWORD=<your password>
```

3. Modify `COURSES` filter & download volume mount target in the `docker-compose.yml` file (See it's comments for more explanation)

4. Start it! `docker compose up -d`

[5. It'll now run every 12h (can be changed, see `docker-compose.yml`) in the background, stop it with: `docker compose down`]

## ToDo

- [x] Add some sort of check summing to only download newly added files

## Development

Disable playwright headless mode with `export DISABLE_HEADLESS=true`
