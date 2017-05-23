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
        """Display information about the current version and counts of entities in the database.

        @:returns json
        """
        return self._get('{}/{}/info'.format(self.url, self.api_version))

    def get_volume_types(self):
        """List volume types.

        @:returns json        
        """
        return self._get('{}/{}/volume_types'.format(self.url, self.api_version))

    def get_volume_type(self, volume_type_id):
        """Get a volume type.

        :arg str volume_type_id: Volume Type Uuid

        :raises ClientError
        @:returns json        
        """
        return self._get('{}/{}/volume_type/{}'.format(self.url, self.api_version, volume_type_id))

    def create_volume_type(self, volume_type_id, volume_type_name):
        """Create a volume type.

        :arg str volume_type_id: The Volume Type id
        :arg str volume_type_name: The Volume Type name

        :raises ClientError
        @:returns str
        """
        url = '{}/{}/volume_type'.format(self.url, self.api_version)
        data = {'type_id': volume_type_id, 'type_name': volume_type_name}
        self._post(url, data)
        return True

    def delete_volume_type(self, volume_type_id):
        """Delete the volume type.

        :arg str volume_type_id: Volume Type Uuid

        :raises ClientError
        @:returns str        
        """
        self._delete('{}/{}/volume_type/{}'.format(self.url, self.api_version, volume_type_id))
        return True

    def get_volumes(self, tenant_id, start, end):
        """List volumes for a tenant.

        :arg Uuid tenant_id: Tenant Uuid
        :arg DateTime start
        :arg DateTime end

        :raises ClientError
        @:returns json        
        """
        url = '{}/{}/project/{}/volumes'.format(self.url, self.api_version, tenant_id)
        params = {'start': self._format_qs_datetime(start), 'end': self._format_qs_datetime(end)}
        return self._get(url, params)

    def get_instances(self, tenant_id, start, end):
        """List instances for a tenant.

        :arg str tenant_id: The Tenant Uuid
        :arg DateTime start
        :arg DateTime end

        :raises ClientError
        @:returns json        
        """
        url = '{}/{}/project/{}/instances'.format(self.url, self.api_version, tenant_id)
        params = {'start': self._format_qs_datetime(start), 'end': self._format_qs_datetime(end)}
        return self._get(url, params)

    def create_instance(self, tenant_id, instance_id, name, flavor, start, image_meta=None):
        """Create an instance for a tenant.

        :arg str tenant_id: The Tenant Uuid
        :arg str instance_id: The instance uuid
        :arg str name: The instance name
        :arg str flavor: The flavor uuid
        :arg DateTime start
        :arg dict image_meta: The OS type, distro and version of the image

        :raises ClientError
        @:returns str        
        """
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
        """Delete the instance.

        :arg str instance_id: Instance Uuid
        :arg DateTime end

        :raises ClientError
        @:returns str        
        """
        data = {'date': self._format_body_datetime(end or datetime.now())}
        self._delete('{}/{}/instance/{}'.format(self.url, self.api_version, instance_id), data=data)
        return True

    def get_tenant_entities(self, tenant_id, start, end):
        """List instances and volumes for a tenant.

        :arg str tenant_id: Tenant Uuid
        :arg DateTime start
        :arg DateTime end

        :raises ClientError
        @:returns json        
        """
        url = '{}/{}/project/{}/entities'.format(self.url, self.api_version, tenant_id)
        params = {'start': self._format_qs_datetime(start), 'end': self._format_qs_datetime(end)}
        return self._get(url, params)

    def update_instance_entity(self, instance_id, **kwargs):
        """Update an instance entity.

        :arg str instance_id: Instance Uuid
        :arg DateTime start
        :arg DateTime end
        :arg str flavor: The flavor uuid
        :arg str name: The instance name

        :raises ClientError
        @:returns str        
        """
        url = '{}/{}/entity/instance/{}'.format(self.url, self.api_version, instance_id)

        for param in ['start', 'end']:
            if param in kwargs:
                kwargs[param] = self._format_body_datetime(kwargs[param])

        return self._put(url, kwargs)

    def _format_body_datetime(self, dt):
        return dt.strftime(self.DATE_FORMAT_BODY)

    def _format_qs_datetime(self, dt):
        return dt.strftime(self.DATE_FORMAT_QS)
