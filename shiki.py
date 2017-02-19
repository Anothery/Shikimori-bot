# -*- coding: utf-8 -*-

import requests
from copy import copy


class Shiki:
    def __init__(self):
        self.root_url = 'https://shikimori.org/api'
        self.request_url = self.root_url
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Shikimori Bot for Telegram'})

    def __getattr__(self, section):
        self.request_url += '/' + section
        return self

    def get(self, last_sect=None, **args):
        if last_sect:
            self.request_url += '/' + str(last_sect)
        return self.session.get(self.clean_request_url(), params=args).json()

    def clean_request_url(self):
        url = copy(self.request_url)
        self.request_url = self.root_url
        return url

