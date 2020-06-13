#!/usr/bin/python
import os
import shlex
import subprocess
from abc import ABC, abstractmethod
import sys
from streamlink_cli import main as streamlink


class AbstractStreamDownloaderService(ABC):
    def __init__(self, folder_path):
        self.OUTPUT_FOLDER = folder_path
        self.BIN_FOLDER = os.path.join(os.environ["VIRTUAL_ENV"], "bin")

    @abstractmethod
    def download(self, video_id, video_name):
        pass


class StreamLinkDownloader(AbstractStreamDownloaderService):

    def download(self, video_id, video_name):
        youtube_url = "https://www.youtube.com/watch?v"
        sys.argv.extend([
            '--hls-live-restart',
             '--output',
            "%s/%s.ts" % (self.OUTPUT_FOLDER, video_name),
            '--url',
            "%s=%s" % (youtube_url, video_id),
            '--default-stream',
            "best"])
        streamlink.main()
