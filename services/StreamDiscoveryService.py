#!/usr/bin/python
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from abc import ABC, abstractmethod


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
    def __init__(self, channel_id, args=None):
        if args is None:
            args = {}
        super().__init__(channel_id)
        self.youtube = build(
            args["YOUTUBE_API_SERVICE_NAME"],
            args["YOUTUBE_API_VERSION"],
            developerKey=args["DEVELOPER_KEY"],
        )

    def search(self):
        search_response = (
            self.youtube.search()
            .list(
                channelId=self.channel_id,
                type="video",
                eventType="live",
                part="snippet",
                maxResults=10,
            )
            .execute()
        )

        items = search_response.get("items", [])
        if len(items) > 0:
            stream_id = items[0]["id"]["videoId"]
            stream_name = items[0]["snippet"]["title"]
            return [stream_id, stream_name]
        return []
