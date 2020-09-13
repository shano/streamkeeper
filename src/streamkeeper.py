#!/usr/bin/python

import argparse
import os
import time
import typing

import daemon

from .config import Config
from .services.ConversionService import AbstractConversionService, FfmpgConversionService
from .services.NotificationService import AbstractNotificationService
from .services.StreamDiscoveryService import AbstractStreamDiscoveryService, YoutubeStreamDiscoveryService
from .services.StreamDownloadService import AbstractStreamDownloaderService, StreamLinkDownloader


class StreamKeeper:
    def __init__(
        self,
        converter: typing.Type[AbstractConversionService],
        stream_discoverer: typing.Type[AbstractStreamDiscoveryService],
        stream_downloader: typing.Type[AbstractStreamDownloaderService],
        notifier: typing.Type[AbstractNotificationService],
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
        self.notifier.notify("Starting streamkeeper")
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
                    if self.config.converstion["ENABLED"]:
                        self.converter.convert(machine_friendly_name, self.config.converstion["OUTPUT_FORMAT"])
                        self.notifier.notify(
                            "Converted video -> %s" % stream_name, title="Stream Converted",
                        )
                time.sleep(self.config.discovery["TIME_BETWEEN_SCAN_SECONDS"])
            except Exception as e:
                self.notifier.notify("Exception happened %s" % repr(e))
                time.sleep(self.config.discovery["TIME_BETWEEN_SCAN_SECONDS"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--run_type",
        dest="run_type",
        choices=["daemon", "process"],
        help="Run as a background daemon",
        default="process",
    )
    parser.add_argument(
        "-c", "--config_file", type=config_file, help="Path to config file", default="false",
    )

    return parser.parse_args()


def config_file(config_file_path):
    full_config_file_path = os.path.join(os.getcwd(), config_file_path)
    try:
        return Config(full_config_file_path)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"readable_file:{full_config_file_path} is not a valid file {str(e)}")


def get_stream_keeper_service(config):
    # Initialise dependencies
    service_converter = FfmpgConversionService(config.path["OUTPUT"])
    try:
        from .services.NotificationService import PushoverNotificationService

        service_notifier = PushoverNotificationService(config.pushover["CLIENT_ID"], config.pushover["TOKEN"])
    except ImportError:
        from .services.NotificationService import PrintNotificationService

        service_notifier = PrintNotificationService()

    service_stream_downloader = StreamLinkDownloader(config.path["OUTPUT"])
    service_stream_discoverer = YoutubeStreamDiscoveryService(
        config.youtube["CHANNEL_ID"],
        {
            "YOUTUBE_API_SERVICE_NAME": config.youtube["API_SERVICE_NAME"],
            "YOUTUBE_API_VERSION": config.youtube["API_VERSION"],
            "DEVELOPER_KEY": config.youtube["DEVELOPER_KEY"],
        },
    )

    return StreamKeeper(
        service_converter, service_stream_discoverer, service_stream_downloader, service_notifier, config
    )


def run_as_daemon():
    args = parse_args()
    streamkeeper = get_stream_keeper_service(args.config_file)
    with daemon.DaemonContext():
        streamkeeper.run()


def run_as_process():
    args = parse_args()
    streamkeeper = get_stream_keeper_service(args.config_file)
    streamkeeper.run()


def main():
    args = parse_args()
    if args.run_type == "daemon":
        run_as_daemon()
    else:
        run_as_process()


if __name__ == "__main__":
    main()
