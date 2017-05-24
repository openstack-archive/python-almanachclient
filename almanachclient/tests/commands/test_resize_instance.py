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

from almanachclient.commands.resize_instance import ResizeInstanceCommand

from almanachclient.tests import base


class TestResizeInstanceCommand(base.TestCase):

    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.app_args = mock.Mock()
        self.args = Namespace(instance_id='some uuid', flavor='some flavor', date=None)

        self.client = mock.Mock()
        self.app.get_client.return_value = self.client
        self.command = ResizeInstanceCommand(self.app, self.app_args)

    def test_execute_command(self):
        self.assertEqual('Success', self.command.take_action(self.args))
        self.client.resize_instance.assert_called_once_with('some uuid', 'some flavor', None)

    def test_execute_command_with_date(self):
        self.args.date = '2017-01-01'
        self.assertEqual('Success', self.command.take_action(self.args))
        self.client.resize_instance.assert_called_once_with('some uuid',
                                                            'some flavor',
                                                            datetime.datetime(2017, 1, 1, 0, 0))
