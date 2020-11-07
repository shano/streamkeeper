#!/usr/bin/python

import argparse
import time
from pathlib import Path
from typing import Type

import daemon

from streamkeeper.services.ConversionService import AbstractConversionService, FfmpgConversionService
from streamkeeper.services.NotificationService import AbstractNotificationService
from streamkeeper.services.StreamDiscoveryService import AbstractStreamDiscoveryService, YoutubeStreamDiscoveryService
from streamkeeper.services.StreamDownloadService import AbstractStreamDownloaderService, StreamLinkDownloader

if Path("config.py").is_file():
    from config import CONVERSION_CONFIG, DISCOVERY_CONFIG, PATH_CONFIG, YOUTUBE_CONFIG


class StreamKeeper:
    def __init__(
        self,
        converter: Type[AbstractConversionService],
        stream_discoverer: Type[AbstractStreamDiscoveryService],
        stream_downloader: Type[AbstractStreamDownloaderService],
        notifier: Type[AbstractNotificationService],
    ):
        self.converter = converter
        self.stream_discoverer = stream_discoverer
        self.stream_downloader = stream_downloader
        self.notifier = notifier

    @staticmethod
    def __unique_machine_name(s):
        return "".join(x for x in s if x.isalnum()) + time.strftime("%Y%m%d-%H%M%S")

    def run(self):
        while True:
            try:
                search_result = self.stream_discoverer.search()
                if search_result:
                    [stream_id, stream_name] = search_result
                    machine_friendly_name = self.__unique_machine_name(stream_name)
                    self.notifier.notify("Downloading video -> %s" % stream_name, title="Stream Started")
                    self.stream_downloader.download(stream_id, machine_friendly_name)
                    self.notifier.notify(
                        "Downloaded video -> %s" % stream_name, title="Stream Downloaded",
                    )
                    if CONVERSION_CONFIG["ENABLED"]:
                        self.converter.convert(machine_friendly_name, CONVERSION_CONFIG["OUTPUT_FORMAT"])
                        self.notifier.notify(
                            "Converted video -> %s" % stream_name, title="Stream Converted",
                        )
                time.sleep(DISCOVERY_CONFIG["TIME_BETWEEN_SCAN_SECONDS"])
            except Exception as e:
                self.notifier.notify("Exception happened %s" % repr(e))
                time.sleep(DISCOVERY_CONFIG["TIME_BETWEEN_SCAN_SECONDS"])

    def start(self, run_type="process"):
        self.notifier.notify("Starting streamkeeper")
        if run_type == "daemon":
            with daemon.DaemonContext():
                self.run()
        else:
            self.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="run_type", choices=["daemon", "process"], help="Run as a background daemon", default="false",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    # Initialise dependencies
    service_converter = FfmpgConversionService(PATH_CONFIG["OUTPUT"])
    try:

        if Path("config.py").is_file():
            from config import PUSHOVER_CONFIG
        from streamkeeper.services.NotificationService import PushoverNotificationService

        service_notifier = PushoverNotificationService(PUSHOVER_CONFIG["CLIENT_ID"], PUSHOVER_CONFIG["TOKEN"])
    except ImportError:
        from streamkeeper.services.NotificationService import PrintNotificationService

        service_notifier = PrintNotificationService()

    service_stream_downloader = StreamLinkDownloader(PATH_CONFIG["OUTPUT"])
    service_stream_discoverer = YoutubeStreamDiscoveryService(
        YOUTUBE_CONFIG["CHANNEL_ID"],
        {
            "YOUTUBE_API_SERVICE_NAME": YOUTUBE_CONFIG["API_SERVICE_NAME"],
            "YOUTUBE_API_VERSION": YOUTUBE_CONFIG["API_VERSION"],
            "DEVELOPER_KEY": YOUTUBE_CONFIG["DEVELOPER_KEY"],
        },
    )

    streamkeeper = StreamKeeper(
        service_converter, service_stream_discoverer, service_stream_downloader, service_notifier,
    )
    streamkeeper.start(args.run_type)


if __name__ == "__main__":
    main()
