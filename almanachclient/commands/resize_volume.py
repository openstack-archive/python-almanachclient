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


class ResizeVolumeCommand(Command):
    """Resize volume"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('volume_id', help='Volume ID')
        parser.add_argument('size', help='Size')
        parser.add_argument('--date', help='Resize date (now if missing)')
        return parser

    def take_action(self, parsed_args):
        self.app.get_client().resize_volume(parsed_args.volume_id,
                                            parsed_args.size,
                                            date_parser.parse(parsed_args.date) if parsed_args.date else None)
        return 'Success'
