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
        response = requests.get(url, headers=self._get_headers(), params=params)
        body = response.json()

        if response.status_code != 200:
            raise exceptions.HTTPError('{} ({})'.format(body.get('error') or 'HTTP Error', response.status_code))

        return body

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-almanachclient/{}'.format(client_version.__version__),
            'X-Auth-Token': self.token,
        }
