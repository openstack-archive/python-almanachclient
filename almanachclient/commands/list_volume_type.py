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


class ListVolumeTypeCommand(Lister):
    """List volume types"""

    columns = ('Volume Type ID', 'Volume Type Name')

    def take_action(self, parsed_args):
        volume_types = self.app.get_client().get_volume_types()
        return self.columns, self._format_volume_types(volume_types)

    def _format_volume_types(self, volume_types):
        rows = []
        for volume_type in volume_types:
            rows.append((volume_type.get('volume_type_id'), volume_type.get('volume_type_name')))
        return rows
