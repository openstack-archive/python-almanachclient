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

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone_client

from almanachclient import exceptions


class KeystoneClient(object):
    def __init__(self, auth_url, username, password, service, region_name,
                 domain_name='default', user_domain_id='default'):
        """KeystoneClient

        :arg str auth_url: Keystone URL (v3 endpoint)
        :arg str username: Username
        :arg str password: Password
        :arg str service: Service name (example: almanach)
        :arg str region_name: Region name
        :arg str domain_name: Domain name
        :arg str user_domain_id: User domain ID
        """
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.service = service
        self.region_name = region_name
        self.domain_name = domain_name
        self.user_domain_id = user_domain_id

    def get_token(self):
        """Get Keystone token

        :rtype: str
        """
        sess = self._get_session()
        return sess.get_token()

    def get_endpoint_url(self, visibility='admin'):
        """Get Almanach API URL from Keystone catalog

        :arg str visibility: Service visibility
        :return: Almanach Endpoint URL
        :rtype: str
        """
        keystone = keystone_client.Client(session=self._get_session())
        endpoints = keystone.endpoints.list(service=self.service, region=self.region_name)

        for endpoint in endpoints:
            if endpoint.interface == visibility:
                return endpoint.url

        raise exceptions.EndpointNotFound('Endpoint URL Not Found')

    def _get_session(self):
        auth = v3.Password(auth_url=self.auth_url,
                           username=self.username,
                           password=self.password,
                           domain_name=self.domain_name,
                           user_domain_id=self.user_domain_id)

        return session.Session(auth=auth)
