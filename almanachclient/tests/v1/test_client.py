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
from almanachclient import version


class TestClient(base.TestCase):

    def setUp(self):
        super().setUp()
        self.response = mock.Mock(headers={'Content-Type': 'application/json; charset=utf-8',
                                           'Content-Length': '1'})
        self.url = 'http://almanach_url'
        self.token = 'token'
        self.headers = {'Content-Type': 'application/json',
                        'User-Agent': 'python-almanachclient/{}'.format(version.__version__),
                        'X-Auth-Token': self.token,
                        'Accept': 'application/json'}

        self.client = Client(self.url, self.token)

        self.session = mock.Mock()
        self.session.get_endpoint.return_value = 'http://almanach_url/from/session'

    def test_instantiate_client_with_a_session(self):
        client = Client(session=self.session)

        self.assertEqual('http://almanach_url/from/session', client.get_url())

        self.session.get_endpoint.called_once_with(service_type='cloudmetrics', region_name=None, interface=None)

    def test_instantiate_client_endpoint_url_override_session_url(self):
        client = Client(url='http://almanach_url', session=self.session)

        self.assertEqual('http://almanach_url', client.get_url())

        self.session.get_endpoint.called_once_with(service_type='cloudmetrics', region_name=None, interface=None)

    def test_instantiate_client_no_url_and_no_session(self):
        self.assertRaises(ValueError, Client)

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

    @mock.patch('requests.get')
    def test_get_tenant_entities_without_end_date(self, requests):
        expected = [mock.Mock()]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        start = datetime.now()
        params = dict(start=start.strftime(Client.DATE_FORMAT_QS))

        self.assertEqual(expected, self.client.get_tenant_entities('my_tenant_id', start))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/my_tenant_id/entities'),
                                         params=params,
                                         headers=self.headers)

    @mock.patch('requests.get')
    def test_get_entity(self, requests):
        expected = [mock.Mock()]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        self.assertEqual(expected, self.client.get_entity('entity_id'))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/entity/entity_id'),
                                         params=None,
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

    @mock.patch('requests.put')
    def test_resize_instance(self, requests):
        date = datetime.now()
        requests.return_value = self.response

        self.response.headers['Content-Length'] = 0
        self.response.status_code = 200

        self.assertTrue(self.client.resize_instance('my_instance_id', 'another flavor', date))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/instance/my_instance_id/resize'),
                                         params=None,
                                         data=json.dumps({'flavor': 'another flavor',
                                                          'date': date.strftime(Client.DATE_FORMAT_BODY)}),
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
        self.response.headers['Content-Length'] = 0

        requests.return_value = self.response
        self.response.status_code = 201

        self.assertTrue(self.client.create_volume_type('some uuid', 'some name'))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_type'),
                                         headers=self.headers,
                                         data=json.dumps(data),
                                         params=None)

    @mock.patch('requests.delete')
    def test_delete_volume_type(self, requests):
        self.response.headers['Content-Length'] = 0

        requests.return_value = self.response
        self.response.status_code = 202

        self.assertTrue(self.client.delete_volume_type('some uuid'))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume_type/some uuid'),
                                         headers=self.headers,
                                         data=None,
                                         params=None)

    @mock.patch('requests.delete')
    def test_delete_instance(self, requests):
        self.response.headers['Content-Length'] = 0
        date = datetime.now()

        requests.return_value = self.response
        self.response.status_code = 202

        self.assertTrue(self.client.delete_instance('some uuid', date))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/instance/some uuid'),
                                         headers=self.headers,
                                         data=json.dumps({'date': date.strftime(Client.DATE_FORMAT_BODY)}),
                                         params=None)

    @mock.patch('requests.post')
    def test_create_instance(self, requests):
        self.response.headers['Content-Length'] = 0
        date = datetime.now()

        requests.return_value = self.response
        self.response.status_code = 201

        self.assertTrue(self.client.create_instance('tenant_id', 'instance_id', 'name', 'flavor', date))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/tenant_id/instance'),
                                         headers=self.headers,
                                         data=mock.ANY,
                                         params=None)

    @mock.patch('requests.get')
    def test_get_instances(self, requests):
        expected = [mock.Mock()]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        start = datetime.now()
        end = datetime.now()
        params = dict(start=start.strftime(Client.DATE_FORMAT_QS), end=end.strftime(Client.DATE_FORMAT_QS))

        self.assertEqual(expected, self.client.get_instances('my_tenant_id', start, end))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/my_tenant_id/instances'),
                                         params=params,
                                         headers=self.headers)

    @mock.patch('requests.get')
    def test_get_volumes(self, requests):
        expected = [mock.Mock()]

        requests.return_value = self.response
        self.response.json.return_value = expected
        self.response.status_code = 200

        start = datetime.now()
        end = datetime.now()
        params = dict(start=start.strftime(Client.DATE_FORMAT_QS), end=end.strftime(Client.DATE_FORMAT_QS))

        self.assertEqual(expected, self.client.get_volumes('my_tenant_id', start, end))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/my_tenant_id/volumes'),
                                         params=params,
                                         headers=self.headers)

    @mock.patch('requests.put')
    def test_resize_volume(self, requests):
        date = datetime.now()
        requests.return_value = self.response

        self.response.headers['Content-Length'] = 0
        self.response.status_code = 200

        self.assertTrue(self.client.resize_volume('my_volume_id', 3, date))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume/my_volume_id/resize'),
                                         params=None,
                                         data=json.dumps({'size': 3,
                                                          'date': date.strftime(Client.DATE_FORMAT_BODY)}),
                                         headers=self.headers)

    @mock.patch('requests.post')
    def test_create_volume(self, requests):
        date = datetime.now()
        requests.return_value = self.response

        self.response.headers['Content-Length'] = 0
        self.response.status_code = 201

        self.assertTrue(self.client.create_volume('tenant_id', 'my_volume_id', 'volume_type_id',
                                                  'volume name', 2, start=date))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/project/tenant_id/volume'),
                                         params=None,
                                         data=json.dumps({
                                             'volume_id': 'my_volume_id',
                                             'volume_type': 'volume_type_id',
                                             'volume_name': 'volume name',
                                             'size': 2,
                                             'attached_to': [],
                                             'start': date.strftime(Client.DATE_FORMAT_BODY),
                                         }),
                                         headers=self.headers)

    @mock.patch('requests.put')
    def test_attach_volume(self, requests):
        date = datetime.now()
        requests.return_value = self.response

        self.response.headers['Content-Length'] = 0
        self.response.status_code = 200

        self.assertTrue(self.client.attach_volume('my_volume_id', ['instance_id'], date))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume/my_volume_id/attach'),
                                         params=None,
                                         data=json.dumps({'attachments': ['instance_id'],
                                                          'date': date.strftime(Client.DATE_FORMAT_BODY)}),
                                         headers=self.headers)

    @mock.patch('requests.put')
    def test_detach_volume(self, requests):
        date = datetime.now()
        requests.return_value = self.response

        self.response.headers['Content-Length'] = 0
        self.response.status_code = 200

        self.assertTrue(self.client.detach_volume('my_volume_id', ['instance_id'], date))

        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume/my_volume_id/detach'),
                                         params=None,
                                         data=json.dumps({'attachments': ['instance_id'],
                                                          'date': date.strftime(Client.DATE_FORMAT_BODY)}),
                                         headers=self.headers)

    @mock.patch('requests.delete')
    def test_delete_volume(self, requests):
        self.response.headers['Content-Length'] = 0
        date = datetime.now()

        requests.return_value = self.response
        self.response.status_code = 202

        self.assertTrue(self.client.delete_volume('some uuid', date))
        requests.assert_called_once_with('{}{}'.format(self.url, '/v1/volume/some uuid'),
                                         headers=self.headers,
                                         data=json.dumps({'date': date.strftime(Client.DATE_FORMAT_BODY)}),
                                         params=None)
