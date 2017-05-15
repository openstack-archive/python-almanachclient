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
    def _get(self, url):
        logger.debug(url)
        response = requests.get(url, headers=self._get_headers())

        if response.status_code != 200:
            raise exceptions.HTTPError('HTTP Error ({})'.format(response.status_code))

        return response.json()

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-almanachclient/{}'.format(client_version.__version__),
        }
