#!/usr/bin/python
from abc import ABC, abstractmethod

from googleapiclient.discovery import build


class AbstractStreamDiscoveryService(ABC):
    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def __init__(self, channel_id, args=None):
        if args is None:
            args = {}
        self.channel_id = channel_id


class YoutubeStreamDiscoveryService(AbstractStreamDiscoveryService):

    youtube = None

    def __init__(self, channel_id, args=None):
        if args is None:
            args = {}
        super().__init__(channel_id)
        self.youtube = build(
            args["YOUTUBE_API_SERVICE_NAME"], args["YOUTUBE_API_VERSION"], developerKey=args["DEVELOPER_KEY"],
        )

    def _api_search(self, **kwargs):
        return self.youtube.search().list(**kwargs)

    def search(self):
        search_response = self._api_search(
            channelId=self.channel_id, type="video", eventType="live", part="snippet", maxResults=10,
        ).execute()

        items = search_response.get("items", [])
        if len(items) > 0:
            stream_id = items[0]["id"]["videoId"]
            stream_name = items[0]["snippet"]["title"]
            return [stream_id, stream_name]
        return []
