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
import datetime
from unittest import mock

from almanachclient.commands.list_entity import ListEntityCommand

from almanachclient.tests import base


class TestListEntityCommand(base.TestCase):

    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.app_args = mock.Mock()
        self.args = Namespace(tenant_id=None, start=None, end=None)

        self.client = mock.Mock()
        self.app.get_client.return_value = self.client
        self.command = ListEntityCommand(self.app, self.app_args)

    def test_execute_command(self):
        self.args.tenant_id = 'some uuid'
        self.args.start = '2017-01-01'
        self.args.end = '2017-01-30'
        self.client.get_tenant_entities.return_value = [{'entity_id': 'some uuid', 'project_id': 'tenant id'}]

        expected = (('Entity ID', 'Type', 'Name', 'Start', 'End', 'Properties'),
                    [('some uuid', None, None, None, None, None)])

        self.assertEqual(expected, self.command.take_action(self.args))

        self.client.get_tenant_entities.assert_called_once_with(self.args.tenant_id,
                                                                datetime.datetime(2017, 1, 1, 0, 0),
                                                                datetime.datetime(2017, 1, 30, 0, 0))

    def test_execute_command_without_end_date(self):
        self.args.tenant_id = 'some uuid'
        self.args.start = '2017-01-01'
        self.client.get_tenant_entities.return_value = [{'entity_id': 'some uuid', 'project_id': 'tenant id'}]

        expected = (('Entity ID', 'Type', 'Name', 'Start', 'End', 'Properties'),
                    [('some uuid', None, None, None, None, None)])

        self.assertEqual(expected, self.command.take_action(self.args))

        self.client.get_tenant_entities.assert_called_once_with(self.args.tenant_id,
                                                                datetime.datetime(2017, 1, 1, 0, 0),
                                                                None)
