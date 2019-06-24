# Streamkeeper

Watch youtube channels and automatically download any live streams they post and convert to a video format. Get notified over pushover.


## Requirements

`pip install -r requirements.txt`

Also requires [ffmpeg](https://ffmpeg.org/) and [streamlink](https://github.com/streamlink/streamlink), both need to be installed and executables in the current path.

## Configuration

For now copy config.py.sample to config.py and fill in following the TODO comments.

## TODO

* Support list of channels
* Add queueing between discovery and downloader
* Better config support
* Better dependency initialisation
* Testing is a pain w/ streams, add unit tests to better test services
* Append timestamp to file name, so repeated stream names aren't an issue
* Research alternative to having to use subprocess for ffpmeg and streamlink
* Create a stream model to represent the state of the stream being downloaded/converted
* Should stop notifications if PUSHOVER not configured
* Support more formats
