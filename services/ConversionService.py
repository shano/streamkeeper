import subprocess
from abc import ABC, abstractmethod


class AbstractConversionService(ABC):
    @abstractmethod
    def convert(self, video_name):
        pass


class FfmpgConversionService(AbstractConversionService):
    def __init__(self, FILE_PATH, type="MP4"):
        self.file_path = FILE_PATH

    def convert(self, video_name):
        command = "ffmpeg -i files/%s.ts -c:v libx264 -c:a aac files/%s.mp4" % (
            video_name,
            video_name,
        )
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
