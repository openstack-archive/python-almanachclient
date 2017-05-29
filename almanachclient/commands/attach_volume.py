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

from dateutil import parser as date_parser

from cliff.command import Command


class AttachVolumeCommand(Command):
    """Attach volume"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('volume_id', help='Volume ID')
        parser.add_argument('--date', help='Start date')
        parser.add_argument('--attachment', action='append', help='Instance attached to the volume')
        return parser

    def take_action(self, parsed_args):
        date = date_parser.parse(parsed_args.date) if parsed_args.date else None
        self.app.get_client().attach_volume(parsed_args.volume_id,
                                            attachments=parsed_args.attachment,
                                            attachment_date=date)
        return 'Success'
