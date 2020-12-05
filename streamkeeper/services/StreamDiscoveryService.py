#!/usr/bin/python
import json
from abc import ABC, abstractmethod
from urllib.request import Request, urlopen


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
        base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
        request = Request("https://www.youtube.com/channel/%s" % channel_id, headers=base_headers)

        html = urlopen(request).read().decode("utf-8")  # nosec
        json_data = self.get_initial_data(html)
        self.content = json.loads(json_data)

    def get_initial_data(self, watch_html):
        initial_data_variable = "var ytInitialData ="
        start_index = watch_html.find(initial_data_variable)
        tmp = watch_html[start_index + len(initial_data_variable) :]
        end_index = tmp.find("}};")
        tmp = tmp[:end_index] + "}}"
        return tmp

    def get_name(self):
        return self.content["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0][
            "videoRenderer"
        ][
            "title"
        ][
            "runs"
        ][
            0
        ][
            "text"
        ]

    def get_video_id(self):
        return self.content["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0][
            "videoRenderer"
        ][
            "videoId"
        ]

    def search(self):
        return [self.get_video_id(), self.get_name()]
