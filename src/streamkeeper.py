#!/usr/bin/python

import time
import typing

from services.StreamDownloadService import AbstractStreamDownloaderService
from services.StreamDiscoveryService import AbstractStreamDiscoveryService
from services.NotificationService import AbstractNotificationService
from services.ConversionService import AbstractConversionService

from services.StreamDiscoveryService import YoutubeStreamDiscoveryService
from services.StreamDownloadService import StreamLinkDownloader

from services.ConversionService import FfmpgConversionService

from config import YOUTUBE_CONFIG, PATH_CONFIG


class StreamKeeper:
    def __init__(
        self,
        converter: typing.Type[AbstractConversionService],
        stream_discoverer: typing.Type[AbstractStreamDiscoveryService],
        stream_downloader: typing.Type[AbstractStreamDownloaderService],
        notifier: typing.Type[AbstractNotificationService],
    ):
        self.converter = converter
        self.stream_discoverer = stream_discoverer
        self.stream_downloader = stream_downloader
        self.notifier = notifier

    @staticmethod
    def __unique_machine_name(s):
        return "".join(x for x in s if x.isalnum()) + time.strftime("%Y%m%d-%H%M%S")

    def start(self):
        self.notifier.notify("Starting streamkeeper")
        while True:
            try:
                search_result = self.stream_discoverer.search()
                if search_result:
                    [stream_id, stream_name] = search_result
                    machine_friendly_name = self.__unique_machine_name(stream_name)
                    self.notifier.notify(
                        "Downloading video -> %s" % stream_name, title="Stream Started"
                    )
                    self.stream_downloader.download(stream_id, machine_friendly_name)
                    self.notifier.notify(
                        "Downloaded video -> %s" % stream_name,
                        title="Stream Downloaded",
                    )
                    self.converter.convert(machine_friendly_name)
                    self.notifier.notify(
                        "Converted video -> %s" % stream_name, title="Stream Converted"
                    )
            except Exception as e:
                self.notifier.notify("Exception happened %s" % e.message)
                time.sleep(1800)

            time.sleep(1800)


def main():
    # Initialise dependencies
    service_converter = FfmpgConversionService(PATH_CONFIG["OUTPUT"])
    try:
        from config import PUSHOVER_CONFIG
        from services.NotificationService import PushoverNotificationService

        service_notifier = PushoverNotificationService(
            PUSHOVER_CONFIG["CLIENT_ID"], PUSHOVER_CONFIG["TOKEN"]
        )
    except ImportError:
        from services.NotificationService import PrintNotificationService

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
        service_converter,
        service_stream_discoverer,
        service_stream_downloader,
        service_notifier,
    )
    streamkeeper.start()


if __name__ == "__main__":
    main()
