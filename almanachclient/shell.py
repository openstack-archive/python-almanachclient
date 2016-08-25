#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""
Command-line interface to the OpenStack Almanach API.
"""

import sys

from cliff import app
from cliff import commandmanager

from almanachclient import version
from almanachclient.v1 import version_cli


class AlmanachCommandManager(commandmanager.CommandManager):
    SHELL_COMMANDS = {
        "version": version_cli.CliVersionShow,
    }

    def load_commands(self, namespace):
        for name, command_class in self.SHELL_COMMANDS.items():
            self.add_command(name, command_class)


class AlmanachApp(app.App):

    def __init__(self):
        super(AlmanachApp, self).__init__(
            description='Almanach command line client',
            version=version.__version__,
            command_manager=AlmanachCommandManager(None),
            deferred_help=True,
        )


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return AlmanachApp().run(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
