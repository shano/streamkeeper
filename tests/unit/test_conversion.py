from services.ConversionService import FfmpgConversionService
from unittest import mock
import collections


def get_mocked_subprocess_popen():
    process_mock = mock.Mock()
    attrs = {"communicate.return_value": ("output", "error")}
    process_mock.configure_mock(**attrs)
    return process_mock


@mock.patch("services.ConversionService.subprocess.Popen")  # TODO
def test_to_to_mp4(mock_subprocess):
    # Assemble
    mock_subprocess.return_value = get_mocked_subprocess_popen()
    ffmpgconversion = FfmpgConversionService("files")
    video_name = "test"

    # Act
    ffmpgconversion.convert(video_name)

    # Assert
    mock_subprocess.assert_called_once_with(
        f"ffmpeg -i files/{video_name}.ts -c:v libx264 -c:a aac files/{video_name}.mp4",
        stdout=-1,
        shell=True,
    )
