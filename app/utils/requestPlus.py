
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests
import json
import lxml
import lxml.html



class requestHistory(object):
    def __init__(self, response):
        self.response = response
        self._text = None
        self._xtext = None
        self.request = None
        self.status_code = None
        self.headers = {}
        self._request_status = None
        self._request_extra = {}
        self._load()
    def set_status(self, value, extra=None):
        self._request_status = value
        if extra is not None:
            self.add_extra(data=extra)
    def get_status(self):
        return self._request_status
    def add_extra(self, data):
        self._request_extra = data
    def get_extra(self):
        return self._request_extra
    def _load(self):
        if isinstance(self.response, requests.models.Response):
            self.status_code = self.response.status_code
            self.request = self.response.request
            self.headers = self.response.headers
    def content(self):
        return self.text()
    def text(self):
        if not self._text:
            self._text = self.response.text
        return self._text
    def xtext(self):
        if not self._xtext:
            temp_text = self.text()
            if temp_text:
                try:
                    xbody = lxml.html.fromstring(temp_text)
                except Exception as err:
                    print(f'requestHistory.xtext exp - {err}')
                else:
                    if xbody:
                        self._xtext = xbody
        return self._xtext
    def json(self):
        try:
            return json.loads(self.text())
        except Exception as err:
            print(f'requestHistory.json exp - {err}')
        return {}

