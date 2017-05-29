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

from unittest import mock

from almanachclient import exceptions
from almanachclient.keystone_client import KeystoneClient
from almanachclient.tests import base


class TestKeystoneClient(base.TestCase):
    def setUp(self):
        super().setUp()
        self.almanach_url = 'http://almanach_url'
        self.auth_url = 'http://keystone_url'
        self.username = 'username'
        self.password = 'password'
        self.service = 'almanach'
        self.region_name = 'some region'
        self.client = KeystoneClient(self.auth_url, self.username, self.password, self.service, self.region_name)

    @mock.patch('keystoneauth1.session.Session')
    def test_get_token(self, session):
        sess = mock.Mock()
        sess.get_token.return_value = 'some token'
        session.return_value = sess
        self.assertEqual('some token', self.client.get_token())
        sess.get_token.assert_called_with()

    @mock.patch('keystoneclient.v3.client.Client')
    def test_get_endpoint_url(self, keystone):
        endpoint_manager = mock.Mock()
        keystone.return_value = endpoint_manager
        endpoint_manager.endpoints.list.return_value = [mock.Mock(interface='admin', url=self.almanach_url)]

        self.assertEqual(self.almanach_url, self.client.get_endpoint_url())

        endpoint_manager.endpoints.list.assert_called_once_with(service=self.service, region=self.region_name)

    @mock.patch('keystoneclient.v3.client.Client')
    def test_get_endpoint_url_not_found(self, keystone):
        keystone.return_value.endpoints.list.return_value = []
        self.assertRaises(exceptions.EndpointNotFound, self.client.get_endpoint_url)
