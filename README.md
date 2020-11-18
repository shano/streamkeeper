# Streamkeeper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Watches configured youtube channels and will automatically download any live streams the youtube channel posts, then this can convert to a particular video format. Optionally you can get notified over pushover.

## Quickstart

For now copy config.ini.sample to config.ini and fill in following the TODO comments.

* `pip install streamkeeper`
* `streamkeeper process /path/to/config.ini` - This runs streamkeeper in the foreground.
* `streamkeeper daemon config.ini` - This runs streamkeeper in the background(where config.ini is in the current folder).

Note: The script requires [ffmpeg](https://ffmpeg.org/) if you wish to enable conversions. So this needs to be installed with it's executable in the current path.

## Development

### Setup

* `make setup`
* `make start` or `make daemon` to background it

### Testing

* `make test`

### Publishing

* `make build`
* `make publish`
