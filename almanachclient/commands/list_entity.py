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

from cliff.lister import Lister
from dateutil import parser


class ListEntityCommand(Lister):
    """Show all entities for a given tenant"""

    columns = ('Entity ID', 'Type', 'Name', 'Start', 'End', 'Properties')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('tenant_id', help='Tenant ID')
        parser.add_argument('start', help='Start Date')
        parser.add_argument('--end', help='End Date')
        return parser

    def take_action(self, parsed_args):
        start = parser.parse(parsed_args.start)
        end = parser.parse(parsed_args.end) if parsed_args.end else None
        entities = self.app.get_client().get_tenant_entities(parsed_args.tenant_id, start, end)
        return self.columns, self._format_rows(entities)

    def _format_rows(self, entities):
        rows = []

        for entity in entities:
            entity_type = entity.get('entity_type')

            if entity_type == 'instance':
                properties = dict(flavor=entity.get('flavor'),
                                  image=entity.get('image_meta', entity.get('os')))
            elif entity_type == 'volume':
                properties = dict(volume_type=entity.get('volume_type'),
                                  size=entity.get('size'),
                                  attached_to=entity.get('attached_to'))
            else:
                properties = None

            rows.append((entity.get('entity_id'), entity_type, entity.get('name'),
                         entity.get('start'), entity.get('end'), properties))
        return rows
