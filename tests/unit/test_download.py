import os
from unittest import mock

from hypothesis import given
from hypothesis.strategies import integers, text

from services.StreamDownloadService import StreamLinkDownloader

from ..helper import get_mocked_subprocess_popen


@mock.patch.dict(os.environ, {"VIRTUAL_ENV": "venv"})
@mock.patch("services.StreamDownloadService.subprocess.Popen")
@given(text(), integers())
def test_download_stream(mock_subprocess, video_name, video_id):
    """Tests a subprocess command is called to download stream

    Arguments:
        mock_subprocess {[Mock]} -- [mocked subprocess popen]
    """
    # Assemble
    mock_subprocess.return_value = get_mocked_subprocess_popen()
    stream_link_downloader = StreamLinkDownloader("files")
    stream_url = f"https://www.youtube.com/watch?v={video_id}"
    expected_arguments = [
        os.path.join(os.environ["VIRTUAL_ENV"], "bin", "streamlink"),
        "--hls-live-restart",
        "-o",
        f"files/{video_name}.ts",
        stream_url,
        "best",
    ]

    # Act
    stream_link_downloader.download(video_id, video_name)

    # Assert
    mock_subprocess.assert_called_with(
        expected_arguments, stdout=-1, shell=False,
    )
