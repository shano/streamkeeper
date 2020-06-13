from services.StreamDiscoveryService import YoutubeStreamDiscoveryService
from unittest import mock


@mock.patch("services.StreamDiscoveryService.build")
def test_discovery_builds_youtube_api_client(mock_discovery_client):
    """Tests discovery client setup

    Arguments:
        mock_discovery_client {[Mock]} -- [mocked discovery client]
    """
    # Assemble
    args = {
        "YOUTUBE_API_SERVICE_NAME": "test",
        "YOUTUBE_API_VERSION": "test",
        "DEVELOPER_KEY": "test",
    }

    # Act
    YoutubeStreamDiscoveryService(channel_id=1234, args=args)

    # Assert

    mock_discovery_client.assert_called_once_with(
        args["YOUTUBE_API_SERVICE_NAME"],
        args["YOUTUBE_API_VERSION"],
        developerKey=args["DEVELOPER_KEY"],
    )


@mock.patch("services.StreamDiscoveryService.YoutubeStreamDiscoveryService._api_search")
@mock.patch("services.StreamDiscoveryService.build")
def test_discovery(mock_discovery_client, mock_api_search):
    """Tests discovery does a valid search

    Arguments:
        mock_discovery_client {[Mock]} -- [mocked discovery client]
        mock_api_search {[Mock]} -- [mocked search call]
    """
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
    mock_api_search.assert_called_once_with(**expected_list_args)
