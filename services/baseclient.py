import requests


class ServiceClient:
    def __init__(self, url):
        self.url = url

        if not url.startswith('http'):
            self.url = 'http://' + url

        self._session = requests.Session()
