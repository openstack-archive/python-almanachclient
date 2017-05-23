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

from argparse import Namespace
from unittest import mock

from almanachclient.commands.get_entity import GetEntityCommand

from almanachclient.tests import base


class TestGetEntityCommand(base.TestCase):

    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.app_args = mock.Mock()
        self.args = Namespace(entity_id='some uuid')

        self.client = mock.Mock()
        self.app.get_client.return_value = self.client
        self.command = GetEntityCommand(self.app, self.app_args)

    def test_execute_command(self):
        self.client.get_entity.return_value = [{'entity_id': 'some uuid', 'project_id': 'tenant id'}]

        expected = (('Tenant ID', 'Type', 'Name', 'Start', 'End', 'Properties'),
                    [('tenant id', None, None, None, None, None)])

        self.assertEqual(expected, self.command.take_action(self.args))
        self.client.get_entity.assert_called_once_with(self.args.entity_id)
