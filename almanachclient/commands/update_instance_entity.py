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

from cliff.show import ShowOne
from dateutil import parser


class UpdateInstanceEntityCommand(ShowOne):
    """Update instance entity"""

    columns = ('Tenant ID', 'Instance ID', 'Start', 'End', 'Name', 'Flavor', 'Image')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('instance_id', help='Instance ID')
        parser.add_argument('--start', help='Start Date')
        parser.add_argument('--end', help='End Date')
        parser.add_argument('--flavor', help='Flavor')
        parser.add_argument('--name', help='Instance Name')
        return parser

    def take_action(self, parsed_args):
        params = self._parse_arguments(parsed_args)
        entity = self.app.get_client().update_instance_entity(parsed_args.instance_id, **params)
        return self.columns, self._format_entity(entity)

    def _parse_arguments(self, parsed_args):
        params = dict()

        if parsed_args.start:
            params['start_date'] = parser.parse(parsed_args.start)

        if parsed_args.end:
            params['end_date'] = parser.parse(parsed_args.end)

        if parsed_args.flavor:
            params['flavor'] = parsed_args.flavor

        if parsed_args.name:
            params['name'] = parsed_args.name

        if len(params) == 0:
            raise RuntimeError('At least one argument must be provided: start, end, flavor or name')

        return params

    def _format_entity(self, entity):
        return (
            entity.get('project_id'),
            entity.get('entity_id'),
            entity.get('start'),
            entity.get('end'),
            entity.get('name'),
            entity.get('flavor'),
            entity.get('image_meta', entity.get('os')),
        )
