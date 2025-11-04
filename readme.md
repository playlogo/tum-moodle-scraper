# TUM Moodle scraper

> DISCLAIMER: The software is currently in super early alpha stage, and could randomly overwrite everything in the exposed `data` folder (it shouldn't, but I take no responsibility!).

> KNOWN BUGS:
>
> - Already downloaded files will get updated if the original file on moodle changes

Automatically regularly scrape your TUM Moodle to download all files.
Useful if combined with (for example) [Syncthing](https://syncthing.net/), to automatically download the lecture slides & exercise sheets to your laptop & tablet.

Bundled into a docker container (docker compose included) to allow easy setup - See [Getting started](#getting-started)

This project has no affiliation with, and is not endorsed by, Technische Universität München (TUM).

## Getting started

1. Clone this repo (ideally to a server running 24/7): `git clone https://github.com/playlogo/tum-moodle-scraper && cd tum-moodle-scraper`
2. Create a `.env` file with your TUM shibboleth login credentials:

```env
USERNAME=<your username>
PASSWORD=<your password>
```

3. Modify `COURSES` filter & download volume mount target in the `docker-compose.yml` file (See it's comments for more explanation)

4. Start it! `docker compose up -d`

[5. It'll now run every 23h (can be changed, see `docker-compose.yml`) in the background, stop it with: `docker compose down`]

## ToDo

- [x] Add some sort of check to only download newly added files
- [ ] Handle automatic file name shorting

## Development

Disable playwright headless mode with `export DISABLE_HEADLESS=true`

Note for myself:

```text
moodle-scraper  | Found new file: Allgemeines/In der Klausur bereitgestellte Referenzmaterialien (falls benötigt)
moodle-scraper  | Found new file: 27. Oktober - 2. November/Ankündigung der Fachschaft Aufruf für Kandidaturen zum Semestersprecher oder Semestersprecherin
moodle-scraper  | Found new file: 27. Oktober - 2. November/Übungsblatt 3 RISC-V Teil 2 – Sprünge und Pointer (mit Platz für Lösungen)
moodle-scraper  | Downloading to: /tmp/moodle-102371/Einführung in d 950837132 (W25_26)_20251031_1837.zip
moodle-scraper  | Unzipping to: /tmp/moodle-102371/extracted

=> Übungsblatt 3 RISC-V Teil 2 – S___inter (mit Platz für Lösungen).pdf
=> Ankündigung der Fachschaft Aufr___recher oder Semestersprecherin.pdf
```
