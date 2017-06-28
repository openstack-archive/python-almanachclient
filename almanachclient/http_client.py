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

    def __init__(self, url=None, token=None,
                 session=None, region_name=None,
                 service_type='cloudmetrics', endpoint_type=None):
        """Initialization of Client object.

        :param string url: The endpoint of the Almanach service. Overrides the session url.
        :param string token: The Almanach X-Auth-Token.
        :param session: A session object that can be used for communication.
        :type session: keystonauth.session.Session
        :param string region_name:
        :param string service_type:
        :param string endpoint_type:
        """
        if not url and not session:
            raise ValueError('A session or an endpoint must be provided')

        if session:
            self.url = session.get_endpoint(service_type=service_type, region_name=region_name, interface=endpoint_type)
        if url:
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
        response = requests.post(url,
                                 headers=self._get_headers(),
                                 params=params,
                                 data=json.dumps(data))
        return self._parse_response(response, 201)

    def _delete(self, url, params=None, data=None):
        logger.debug(url)
        response = requests.delete(url,
                                   headers=self._get_headers(),
                                   params=params,
                                   data=json.dumps(data) if data else None)
        return self._parse_response(response, 202)

    def _parse_response(self, response, expected_status=200):
        if response.status_code != expected_status:
            raise exceptions.HTTPError('{} ({})'.format(self._get_error_message(response), response.status_code))

        return self._get_body(response)

    def _get_body(self, response):
        if self._is_json_response(response) and self._has_content(response):
            return response.json()
        return ''

    def _get_error_message(self, response, default_message='HTTP Error'):
        body = self._get_body(response)
        return body.get('error', default_message) if isinstance(body, dict) else response.text

    def _is_json_response(self, response):
        return 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']

    def _has_content(self, response):
        return 'Content-Length' in response.headers and int(response.headers['Content-Length']) > 0

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-almanachclient/{}'.format(client_version.__version__),
            'X-Auth-Token': self.token,
        }
