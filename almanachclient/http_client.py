# Copyright 2017 INAP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import json
import logging

import requests

from almanachclient import exceptions
from almanachclient import version as client_version

logger = logging.getLogger(__name__)


class HttpClient(metaclass=abc.ABCMeta):

    def __init__(self, url, token=None):
        self.url = url
        self.token = token

    def _get(self, url, params=None):
        logger.debug(url)
        return self._parse_response(requests.get(url, headers=self._get_headers(), params=params))

    def _put(self, url, data, params=None):
        logger.debug(url)
        return self._parse_response(requests.put(url,
                                                 headers=self._get_headers(),
                                                 params=params,
                                                 data=json.dumps(data)))

    def _post(self, url, data, params=None):
        logger.debug(url)
        return self._parse_response(requests.post(url,
                                                  headers=self._get_headers(),
                                                  params=params,
                                                  data=json.dumps(data)), 201)

    def _delete(self, url, params=None):
        logger.debug(url)
        return self._parse_response(requests.delete(url, headers=self._get_headers(), params=params), 202)

    def _parse_response(self, response, expected_status=200):
        body = response.json() if len(response.text) > 0 else ''

        if response.status_code != expected_status:
            raise exceptions.HTTPError('{} ({})'.format(body.get('error') or 'HTTP Error', response.status_code))

        return body

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-almanachclient/{}'.format(client_version.__version__),
            'X-Auth-Token': self.token,
        }
