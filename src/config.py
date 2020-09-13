#!/usr/bin/python
import json


class Config:
    def __init__(self, path):
        self.load(path)

    def load(self, path):
        with open(path) as config_file:
            self.config = json.load(config_file)

    @property
    def youtube(self):
        return self.config["YOUTUBE_CONFIG"]

    @property
    def pushover(self):
        return self.config["PUSHOVER_CONFIG"]

    @property
    def path(self):
        return self.config["PATH_CONFIG"]

    @property
    def discovery(self):
        return self.config["DISCOVERY_CONFIG"]

    @property
    def conversion(self):
        return self.config["CONVERSION_CONFIG"]
