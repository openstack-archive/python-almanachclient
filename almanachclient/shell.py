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

import os
import sys

from cliff import app
from cliff import commandmanager

from almanachclient.commands.create_instance import CreateInstanceCommand
from almanachclient.commands.create_volume_type import CreateVolumeTypeCommand
from almanachclient.commands.delete_instance import DeleteInstanceCommand
from almanachclient.commands.delete_volume_type import DeleteVolumeTypeCommand
from almanachclient.commands.endpoint import EndpointCommand
from almanachclient.commands.get_volume_type import GetVolumeTypeCommand
from almanachclient.commands.list_entity import ListEntityCommand
from almanachclient.commands.list_instance import ListInstanceCommand
from almanachclient.commands.list_volume_type import ListVolumeTypeCommand
from almanachclient.commands.list_volumes import ListVolumeCommand
from almanachclient.commands.update_instance_entity import UpdateInstanceEntityCommand
from almanachclient.commands.version import VersionCommand
from almanachclient.keystone_client import KeystoneClient
from almanachclient.v1.client import Client
from almanachclient import version as client_version


class AlmanachCommandManager(commandmanager.CommandManager):
    SHELL_COMMANDS = {
        'version': VersionCommand,
        'endpoint': EndpointCommand,
        'create-volume-type': CreateVolumeTypeCommand,
        'delete-volume-type': DeleteVolumeTypeCommand,
        'list-volume-types': ListVolumeTypeCommand,
        'get-volume-type': GetVolumeTypeCommand,
        'list-volumes': ListVolumeCommand,
        'list-instances': ListInstanceCommand,
        'create-instance': CreateInstanceCommand,
        'delete-instance': DeleteInstanceCommand,
        'list-entities': ListEntityCommand,
        'update instance': UpdateInstanceEntityCommand,
    }

    def load_commands(self, namespace):
        for name, command_class in self.SHELL_COMMANDS.items():
            self.add_command(name, command_class)


class AlmanachApp(app.App):

    def __init__(self):
        super().__init__(
            description='Almanach Command Line Client',
            version=client_version.__version__,
            command_manager=AlmanachCommandManager(None),
            deferred_help=True,
        )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super().build_option_parser(description, version, argparse_kwargs)

        parser.add_argument('--os-auth-url',
                            default=os.environ.get('OS_AUTH_URL'),
                            help='Keystone V3 URL (Env: OS_AUTH_URL).')

        parser.add_argument('--os-region-name',
                            default=os.environ.get('`'),
                            help='OpenStack region name (Env: OS_REGION_NAME).')

        parser.add_argument('--os-password',
                            default=os.environ.get('OS_PASSWORD'),
                            help='OpenStack password (Env: OS_PASSWORD).')

        parser.add_argument('--os-username',
                            default=os.environ.get('OS_USERNAME'),
                            help='OpenStack username (Env: OS_USERNAME).')

        parser.add_argument('--almanach-service',
                            default=os.environ.get('ALMANACH_SERVICE', 'almanach'),
                            help='Almanach keystone service name (Env: ALMANACH_SERVICE).')

        parser.add_argument('--almanach-token',
                            default=os.environ.get('ALMANACH_TOKEN'),
                            help='Almanach API token (Env: ALMANACH_TOKEN).')

        parser.add_argument('--almanach-url',
                            default=os.environ.get('ALMANACH_URL'),
                            help='Almanach API base URL (Env: ALMANACH_URL).')
        return parser

    def get_client(self):
        return Client(self.get_almanach_url(), token=self.options.almanach_token)

    def get_almanach_url(self):
        if self.options.almanach_url:
            return self.options.almanach_url

        keystone = KeystoneClient(auth_url=self.options.os_auth_url,
                                  username=self.options.os_username,
                                  password=self.options.os_password,
                                  service=self.options.almanach_service,
                                  region_name=self.options.os_region_name)

        return keystone.get_endpoint_url()


def main(argv=sys.argv[1:]):
    return AlmanachApp().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
