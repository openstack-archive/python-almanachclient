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

from almanachclient.commands.delete_volume import DeleteVolumeCommand

from almanachclient.tests import base


class TestDeleteVolumeCommand(base.TestCase):

    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.app_args = mock.Mock()
        self.args = Namespace(volume_id='some uuid', end=None)

        self.client = mock.Mock()
        self.app.get_client.return_value = self.client
        self.command = DeleteVolumeCommand(self.app, self.app_args)

    def test_execute_command(self):
        self.assertEqual('Success', self.command.take_action(self.args))
        self.client.delete_volume.assert_called_once_with('some uuid', None)

    def test_execute_command_with_date(self):
        self.args.end = '2017-01-01'
        self.assertEqual('Success', self.command.take_action(self.args))
        self.client.delete_volume.assert_called_once_with('some uuid', datetime.datetime(2017, 1, 1, 0, 0))
