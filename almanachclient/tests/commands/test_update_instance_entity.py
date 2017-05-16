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


from almanachclient.commands.update_instance_entity import UpdateInstanceEntityCommand

from almanachclient.tests import base


class TestUpdateInstanceEntityCommand(base.TestCase):

    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.app_args = mock.Mock()
        self.args = Namespace(instance_id=None, start=None, end=None, flavor=None, name=None)

        self.client = mock.Mock()
        self.app.get_client.return_value = self.client
        self.command = UpdateInstanceEntityCommand(self.app, self.app_args)

    def test_without_required_params(self):
        self.assertRaises(RuntimeError, self.command.take_action, self.args)

    def test_without_optional_params(self):
        self.args.instance_id = 'some uuid'
        self.assertRaises(RuntimeError, self.command.take_action, self.args)

    def test_with_date_arguments(self):
        self.args.instance_id = 'some uuid'
        self.args.start = '2017-01-01'
        self.client.update_instance_entity.return_value = {'entity_id': 'some uuid', 'project_id': 'tenant id'}

        expected = (('Tenant ID', 'Instance ID', 'Start', 'End', 'Name', 'Flavor', 'Image'),
                    ('tenant id', 'some uuid', None, None, None, None, None))

        self.assertEqual(expected, self.command.take_action(self.args))

        self.client.update_instance_entity.assert_called_once_with(self.args.instance_id,
                                                                   start=datetime.datetime(2017, 1, 1, 0, 0))
