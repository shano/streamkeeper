from unittest import mock

from streamkeeper.services.StreamDownloadService import StreamLinkDownloader

from ..helper import get_mocked_subprocess_popen


@mock.patch("streamkeeper.services.StreamDownloadService.subprocess.Popen")
def test_download_stream(mock_subprocess):
    """Tests a subprocess command is called to download stream

    Arguments:
        mock_subprocess {[Mock]} -- [mocked subprocess popen]
    """
    # Assemble
    mock_subprocess.return_value = get_mocked_subprocess_popen()
    stream_link_downloader = StreamLinkDownloader("files")
    video_name = "test"
    video_id = "1234"
    stream_url = f"https://www.youtube.com/watch?v={video_id}"
    expected_arguments = [
        "streamlink",
        "--hls-live-restart",
        "-o",
        f"files/{video_name}.ts",
        stream_url,
        "best",
    ]

    # Act
    stream_link_downloader.download(video_id, video_name)

    # Assert
    mock_subprocess.assert_called_once_with(
        expected_arguments, stdout=-1, shell=False,
    )
