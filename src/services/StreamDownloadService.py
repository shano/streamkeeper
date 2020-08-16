#!/usr/bin/python
import os
import shlex
import subprocess  # nosec - Apart of later fix
from abc import ABC, abstractmethod


class AbstractStreamDownloaderService(ABC):
    def __init__(self, folder_path):
        self.OUTPUT_FOLDER = folder_path
        self.BIN_FOLDER = os.path.join(os.environ["VIRTUAL_ENV"], "bin")

    @abstractmethod
    def download(self, video_id, video_name):
        pass


class StreamLinkDownloader(AbstractStreamDownloaderService):
    def download(self, video_id, video_name):
        streamlink_bin = os.path.join(self.BIN_FOLDER, "streamlink")
        youtube_url = "https://www.youtube.com/watch?v"
        command = '%s --hls-live-restart -o "%s/%s.ts" "%s=%s" best' % (
            streamlink_bin,
            self.OUTPUT_FOLDER,
            video_name,
            youtube_url,
            video_id,
        )
        p = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE)  # nosec - Apart of later fix
        p.communicate()
        p.wait()
