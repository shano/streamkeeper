#!/usr/bin/python

import argparse
import time
from configparser import ConfigParser
from typing import Type

import daemon

from streamkeeper.services.ConversionService import AbstractConversionService, FfmpgConversionService
from streamkeeper.services.NotificationService import AbstractNotificationService
from streamkeeper.services.StreamDiscoveryService import AbstractStreamDiscoveryService, YoutubeStreamDiscoveryService
from streamkeeper.services.StreamDownloadService import AbstractStreamDownloaderService, StreamLinkDownloader


class StreamKeeper:
    def __init__(
        self,
        converter: Type[AbstractConversionService],
        stream_discoverer: Type[AbstractStreamDiscoveryService],
        stream_downloader: Type[AbstractStreamDownloaderService],
        notifier: Type[AbstractNotificationService],
        config,
    ):
        self.converter = converter
        self.stream_discoverer = stream_discoverer
        self.stream_downloader = stream_downloader
        self.notifier = notifier
        self.config = config

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
                    if self.config["CONVERSION"].getboolean("ENABLED"):
                        self.converter.convert(machine_friendly_name, self.config["CONVERSION"]["OUTPUT_FORMAT"])
                        self.notifier.notify(
                            "Converted video -> %s" % stream_name, title="Stream Converted",
                        )
                time.sleep(int(self.config["DISCOVERY"]["TIME_BETWEEN_SCAN_SECONDS"]))
            except Exception as e:
                self.notifier.notify("Exception happened %s" % repr(e))
                time.sleep(int(self.config["DISCOVERY"]["TIME_BETWEEN_SCAN_SECONDS"]))

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
    parser.add_argument(
        dest="config_file", help="Full path to config.ini file", default="config.ini",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    # Initialise dependencies
    config = ConfigParser()
    config.read(args.config_file)
    service_converter = FfmpgConversionService(config["PATH"]["OUTPUT"])
    if "PUSHOVER" in config.sections():
        from streamkeeper.services.NotificationService import PushoverNotificationService

        service_notifier = PushoverNotificationService(config["PUSHOVER"]["CLIENT_ID"], config["PUSHOVER"]["TOKEN"])
    else:
        from streamkeeper.services.NotificationService import PrintNotificationService

        service_notifier = PrintNotificationService()

    service_stream_downloader = StreamLinkDownloader(config["PATH"]["OUTPUT"])
    service_stream_discoverer = YoutubeStreamDiscoveryService(
        config["YOUTUBE"]["CHANNEL_ID"],
        {
            "YOUTUBE_API_SERVICE_NAME": config["YOUTUBE"]["API_SERVICE_NAME"],
            "YOUTUBE_API_VERSION": config["YOUTUBE"]["API_VERSION"],
            "DEVELOPER_KEY": config["YOUTUBE"]["DEVELOPER_KEY"],
        },
    )

    streamkeeper = StreamKeeper(
        service_converter, service_stream_discoverer, service_stream_downloader, service_notifier, config,
    )
    streamkeeper.start(args.run_type)


if __name__ == "__main__":
    main()
