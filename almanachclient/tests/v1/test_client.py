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

from almanachclient.tests import base
from almanachclient.v1.client import Client


class TestClient(base.TestCase):
    def setUp(self):
        super().setUp()
        self.almanach_url = 'http://almanach_url'
        self.client = Client(self.almanach_url)

    @mock.patch('requests.get')
    def test_get_info(self, requests):
        response = mock.Mock()
        expected = {
            'info': {'version': '1.2.3'},
            "database": {'all_entities': 2, 'active_entities': 1}
        }

        requests.return_value = response
        response.json.return_value = expected
        response.status_code = 200

        self.assertEqual(expected, self.client.get_info())
