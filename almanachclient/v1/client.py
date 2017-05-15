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

from almanachclient.http_client import HttpClient


class Client(HttpClient):
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    api_version = 'v1'

    def get_url(self):
        return self.url

    def get_info(self):
        return self._get('{}/{}/info'.format(self.url, self.api_version))

    def get_tenant_entities(self, tenant_id, start, end):
        url = '{}/{}/project/{}/entities'.format(self.url, self.api_version, tenant_id)
        params = {'start': start.strftime(self.DATE_FORMAT), 'end': end.strftime(self.DATE_FORMAT)}
        return self._get(url, params)
