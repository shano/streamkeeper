from services.ConversionService import FfmpgConversionService
from unittest import mock


def get_mocked_subprocess_popen():
    """Get a mocked subprocess popen for testing

    Returns:
        Mock -- mock to be used
    """
    process_mock = mock.Mock()
    attrs = {"communicate.return_value": ("output", "error")}
    process_mock.configure_mock(**attrs)
    return process_mock


@mock.patch("services.ConversionService.subprocess.Popen")
def test_to_to_mp4(mock_subprocess):
    """Tests a subprocess command is called to convert stream

    Arguments:
        mock_subprocess {[Mock]} -- [mocked subprocess popen]
    """
    # Assemble
    mock_subprocess.return_value = get_mocked_subprocess_popen()
    ffmpgconversion = FfmpgConversionService("files")
    video_name = "test"

    # Act
    ffmpgconversion.convert(video_name)

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
    # Assert
    mock_subprocess.assert_called_once_with(
        expected_arguments, stdout=-1, shell=False,
    )
