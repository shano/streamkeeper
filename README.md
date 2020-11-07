[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Streamkeeper

Watches specified youtube channels and will automatically download any live streams the youtube channel posts, then converts to a video format. Optionally you can get notified over pushover.


## Requirements

`make setup`

Also requires [ffmpeg](https://ffmpeg.org/) and [streamlink](https://github.com/streamlink/streamlink), both need to be installed and executables in the current path.

## Configuration

For now copy config.ini.sample to config.ini and fill in following the TODO comments.


## Usage

* `make build`
* `make start` or `make daemon` to background it
