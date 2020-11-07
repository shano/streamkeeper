from unittest import mock

from streamkeeper.services.ConversionService import FfmpgConversionService

from ..helper import get_mocked_subprocess_popen


@mock.patch("streamkeeper.services.ConversionService.subprocess.Popen")
def test_conversion_to_mp4(mock_subprocess):
    """Tests a subprocess command is called to convert stream

    Arguments:
        mock_subprocess {[Mock]} -- [mocked subprocess popen]
    """
    # Assemble
    mock_subprocess.return_value = get_mocked_subprocess_popen()
    ffmpgconversion = FfmpgConversionService("files")
    video_name = "test"
    expected_arguments = [
        "ffmpeg",
        "-i",
        f"files/{video_name}.ts",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        f"files/{video_name}.mp4",
    ]

    # Act
    ffmpgconversion.convert(video_name)

    # Assert
    mock_subprocess.assert_called_once_with(
        expected_arguments, stdout=-1, shell=False,
    )
