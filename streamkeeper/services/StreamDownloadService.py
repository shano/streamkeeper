#!/usr/bin/python
import shlex
import subprocess  # nosec - Apart of later fix
from abc import ABC, abstractmethod


class AbstractStreamDownloaderService(ABC):
    def __init__(self, folder_path):
        self.OUTPUT_FOLDER = folder_path

    @abstractmethod
    def download(self, video_id, video_name):
        pass


class StreamLinkDownloader(AbstractStreamDownloaderService):
    def download(self, video_id, video_name):
        youtube_url = "https://www.youtube.com/watch?v"
        command = 'streamlink --hls-live-restart -o "%s/%s.ts" "%s=%s" best' % (
            self.OUTPUT_FOLDER,
            video_name,
            youtube_url,
            video_id,
        )
        p = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE)  # nosec - Apart of later fix
        p.communicate()
        p.wait()
