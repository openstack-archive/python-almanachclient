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

from datetime import datetime
import json
from unittest import mock

from almanachclient import exceptions
from almanachclient.tests import base
from almanachclient.v1.client import Client


class TestClient(base.TestCase):

    def setUp(self):
        super().setUp()
        self.response = mock.Mock(text='sample data')
        self.url = 'http://almanach_url'
        self.token = 'token'
        self.headers = {'Content-Type': 'application/json',
                        'User-Agent': 'python-almanachclient/0.0.1',
                        'X-Auth-Token': self.token,
                        'Accept': 'application/json'}

        self.client = Client(self.url, self.token)

    @mock.patch('requests.get')
    def test_get_info(self, requests):
        expected = {
            'info': {'version': '1.2.3'},
            "database": {'all_entities': 2, 'active_entities': 1}
        }

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        self.assertEqual(expected, self.client.get_info())
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/info'), headers=self.headers, params=None)

    @mock.patch('requests.get')
    def test_get_info_with_http_error(self, requests):
        requests.return_value = self.response
        self.response.status_code = 500

        self.assertRaises(exceptions.HTTPError, self.client.get_info)

    @mock.patch('requests.get')
    def test_get_tenant_entities(self, requests):
        expected = [mock.Mock()]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        start = datetime.now()
        end = datetime.now()
        params = dict(start=start.strftime(Client.DATE_FORMAT_QS), end=end.strftime(Client.DATE_FORMAT_QS))

        self.assertEqual(expected, self.client.get_tenant_entities('my_tenant_id', start, end))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/my_tenant_id/entities'),
                                         params=params,
                                         headers=self.headers)

    @mock.patch('requests.put')
    def test_update_instance_entity(self, requests):
        expected = dict(name='some entity')

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        self.assertEqual(expected, self.client.update_instance_entity('my_instance_id', name='some entity'))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/entity/instance/my_instance_id'),
                                         params=None,
                                         data=json.dumps({'name': 'some entity'}),
                                         headers=self.headers)

    @mock.patch('requests.get')
    def test_get_volume_types(self, requests):
        expected = [{'volume_type_id': 'some uuid', 'volume_type_name': 'some volume'}]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        self.assertEqual(expected, self.client.get_volume_types())
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_types'),
                                         headers=self.headers, params=None)

    @mock.patch('requests.get')
    def test_get_volume_type(self, requests):
        expected = [{'volume_type_id': 'some uuid', 'volume_type_name': 'some volume'}]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        self.assertEqual(expected, self.client.get_volume_type('some-uuid'))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_type/some-uuid'),
                                         headers=self.headers, params=None)

    @mock.patch('requests.post')
    def test_create_volume_type(self, requests):
        data = {'type_id': 'some uuid', 'type_name': 'some name'}
        self.response.text = ''

        requests.return_value = self.response
        self.response.status_code = 201

        self.assertTrue(self.client.create_volume_type('some uuid', 'some name'))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_type'),
                                         headers=self.headers,
                                         data=json.dumps(data),
                                         params=None)

    @mock.patch('requests.delete')
    def test_delete_volume_type(self, requests):
        self.response.text = ''

        requests.return_value = self.response
        self.response.status_code = 202

        self.assertTrue(self.client.delete_volume_type('some uuid'))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_type/some uuid'),
                                         headers=self.headers,
                                         params=None)
