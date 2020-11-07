import shlex
import subprocess  # nosec - Apart of later fix
from abc import ABC, abstractmethod


class AbstractConversionService(ABC):
    @abstractmethod
    def convert(self, video_name, output_type):
        pass


class FfmpgConversionService(AbstractConversionService):
    def __init__(self, FILE_PATH):
        self.file_path = FILE_PATH

    def convert(self, video_name, output_type="mp4"):
        command = "ffmpeg -i files/%s.ts -c:v libx264 -c:a aac files/%s.%s" % (video_name, video_name, output_type,)
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell=False)  # nosec - Apart of later fix
        p.communicate()
        p.wait()
