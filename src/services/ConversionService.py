import subprocess
from abc import ABC, abstractmethod
import shlex


class AbstractConversionService(ABC):
    @abstractmethod
    def convert(self, video_name):
        pass


class FfmpgConversionService(AbstractConversionService):
    def __init__(self, FILE_PATH, output_type="mp4"):
        self.file_path = FILE_PATH
        self.output_type = output_type

    def convert(self, video_name):
        command = "ffmpeg -i files/%s.ts -c:v libx264 -c:a aac files/%s.%s" % (
            video_name,
            video_name,
            self.output_type,
        )
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell=False)
        p.communicate()
        p.wait()
