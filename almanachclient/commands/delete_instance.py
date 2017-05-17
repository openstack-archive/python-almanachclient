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

from cliff.command import Command
from dateutil import parser as date_parser


class DeleteInstanceCommand(Command):
    """Delete instance"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('instance_id', help='Instance ID')
        parser.add_argument('--end', help='End date')
        return parser

    def take_action(self, parsed_args):
        self.app.get_client().delete_instance(parsed_args.instance_id,
                                              date_parser.parse(parsed_args.end) if parsed_args.end else None)
        return 'Success'
