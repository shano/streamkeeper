from services.StreamDiscoveryService import YoutubeStreamDiscoveryService
from unittest import mock
from unittest.mock import MagicMock
import os


@mock.patch("services.StreamDiscoveryService.build")
def test_discovery(mock_discovery_client):
    """Tests discovery returns results

    Arguments:
        mock_subprocess {[Mock]} -- [mocked subprocess popen]
    """
    execute_mock = MagicMock()
    execute_mock.get().return_value = []
    list_mock = MagicMock()
    list_mock.search().list().return_value = execute_mock
    mock_discovery_client.return_value = list_mock
    # Assemble
    args = {
        "YOUTUBE_API_SERVICE_NAME": "test",
        "YOUTUBE_API_VERSION": "test",
        "DEVELOPER_KEY": "test",
    }

    yt_discovery = YoutubeStreamDiscoveryService(channel_id=1234, args=args)

    # Act
    yt_discovery.search()

    # Assert
    expected_list_args = {
        "channelId": 1234,
        "type": "video",
        "eventType": "live",
        "part": "snippet",
        "maxResults": 10,
    }
    mock_discovery_client.assert_called_once_with(
        args["YOUTUBE_API_SERVICE_NAME"],
        args["YOUTUBE_API_VERSION"],
        developerKey=args["DEVELOPER_KEY"],
    )
    # list_mock.search().list().assert_called_once()
    # list_mock.assert_called_once_with(expected_list_args)
