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

from datetime import datetime

from almanachclient.http_client import HttpClient


class Client(HttpClient):
    DATE_FORMAT_QS = '%Y-%m-%d %H:%M:%S.%f'
    DATE_FORMAT_BODY = '%Y-%m-%dT%H:%M:%S.%fZ'

    api_version = 'v1'

    def get_url(self):
        return self.url

    def get_info(self):
        return self._get('{}/{}/info'.format(self.url, self.api_version))

    def get_volume_types(self):
        return self._get('{}/{}/volume_types'.format(self.url, self.api_version))

    def get_volume_type(self, volume_type_id):
        return self._get('{}/{}/volume_type/{}'.format(self.url, self.api_version, volume_type_id))

    def create_volume_type(self, volume_type_id, volume_type_name):
        url = '{}/{}/volume_type'.format(self.url, self.api_version)
        data = {'type_id': volume_type_id, 'type_name': volume_type_name}
        self._post(url, data)
        return True

    def delete_volume_type(self, volume_type_id):
        self._delete('{}/{}/volume_type/{}'.format(self.url, self.api_version, volume_type_id))
        return True

    def get_instances(self, tenant_id, start, end):
        url = '{}/{}/project/{}/instances'.format(self.url, self.api_version, tenant_id)
        params = {'start': self._format_qs_datetime(start), 'end': self._format_qs_datetime(end)}
        return self._get(url, params)

    def create_instance(self, tenant_id, instance_id, name, flavor, start, image_meta=None):
        url = '{}/{}/project/{}/instance'.format(self.url, self.api_version, tenant_id)
        image_meta = image_meta or {}
        self._post(url, data={
            'id': instance_id,
            'created_at': self._format_body_datetime(start),
            'name': name,
            'flavor': flavor,
            'os_distro': image_meta.get('distro'),
            'os_version': image_meta.get('version'),
            'os_type': image_meta.get('type'),
        })
        return True

    def delete_instance(self, instance_id, end=None):
        data = {'date': self._format_body_datetime(end or datetime.now())}
        self._delete('{}/{}/instance/{}'.format(self.url, self.api_version, instance_id), data=data)
        return True

    def get_tenant_entities(self, tenant_id, start, end):
        url = '{}/{}/project/{}/entities'.format(self.url, self.api_version, tenant_id)
        params = {'start': self._format_qs_datetime(start), 'end': self._format_qs_datetime(end)}
        return self._get(url, params)

    def update_instance_entity(self, instance_id, **kwargs):
        url = '{}/{}/entity/instance/{}'.format(self.url, self.api_version, instance_id)

        for param in ['start', 'end']:
            if param in kwargs:
                kwargs[param] = self._format_body_datetime(kwargs[param])

        return self._put(url, kwargs)

    def _format_body_datetime(self, dt):
        return dt.strftime(self.DATE_FORMAT_BODY)

    def _format_qs_datetime(self, dt):
        return dt.strftime(self.DATE_FORMAT_QS)
