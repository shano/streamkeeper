from unittest import mock

from streamkeeper.services.StreamDiscoveryService import YoutubeStreamDiscoveryService


@mock.patch(
    "streamkeeper.services.StreamDiscoveryService.YoutubeStreamDiscoveryService.get_initial_data",
    mock.Mock(return_value="{}"),
)
@mock.patch("streamkeeper.services.StreamDiscoveryService.urlopen", mock.Mock())
@mock.patch("streamkeeper.services.StreamDiscoveryService.Request")
def test_makes_correct_url_call(mock_request):
    """Tests discovery does a valid search

    Arguments:
        mock_discovery_client {[Mock]} -- [mocked discovery client]
        mock_api_search {[Mock]} -- [mocked search call]
    """
    # Assemble

    # Act
    YoutubeStreamDiscoveryService(channel_id=1234)

    # Assert
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    mock_request.assert_called_once_with("https://www.youtube.com/channel/1234", headers=base_headers)
