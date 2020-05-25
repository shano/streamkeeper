#!/usr/bin/python
import youtube_dl
import subprocess
import time
from abc import ABC, abstractmethod


class AbstractStreamDownloaderService(ABC):
    def __init__(self, folder_path):
        self.FOLDER_PATH = folder_path

    @abstractmethod
    def download(self, video_id, video_name):
        pass


class YTDLDownloader(AbstractStreamDownloaderService):
    def download(self, video_id, video_name):
        ydl = youtube_dl.YoutubeDL({"outtmpl": "%(id)s%(ext)s"})
        with ydl:
            result = ydl.extract_info(
                "http://www.youtube.com/watch?v=%s" % video_id,
                download=True,  # We just want to extract the info
            )


class StreamLinkDownloader(AbstractStreamDownloaderService):
    def download(self, video_id, video_name):
        command = (
            'streamlink --hls-live-restart -o "%s/%s.ts" "https://www.youtube.com/watch?v=%s" best'
            % (self.FOLDER_PATH, video_name, video_id)
        )
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
