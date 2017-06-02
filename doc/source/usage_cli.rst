Command Line Usage
==================

Environment variables
---------------------

* :code:`OS_AUTH_URL`: Keystone URL (v3 endpoint)
* :code:`OS_REGION_NAME`: OpenStack region name
* :code:`OS_USERNAME`: OpenStack username
* :code:`OS_PASSWORD`: OpenStack password
* :code:`ALMANACH_SERVICE`: Almanach Keystone catalog service name
* :code:`ALMANACH_TOKEN`: Almanach API token, if empty a token will be fetched from Keystone
* :code:`ALMANACH_URL`: Almanach API base URL, if empty the endpoint will be fetched from Keystone catalog

Optional Arguments
------------------

* :code:`--os-auth-url`: Keystone URL (v3 endpoint)
* :code:`--os-region-name`: OpenStack region name
* :code:`--os-username`: OpenStack username
* :code:`--os-password`: OpenStack password
* :code:`--almanach-service`: Almanach Keystone catalog service name
* :code:`--almanach-token`: Almanach API token, if empty a token will be fetched from Keystone
* :code:`--almanach-url`: Almanach API base URL, if empty the endpoint will be fetched from Keystone catalog

Get server version
------------------

Usage: :code:`almanach version`

.. code:: bash

    almanach version

    4.0.9

Get Endpoint URL
----------------

Usage: :code:`almanach endpoint`

.. code:: bash

    almanach endpoint

    http://almanach.example.org

Get Tenant Entities
-------------------

Usage: :code:`almanach list-entities <tenant_id> <start> --end <end>`

.. code:: bash

    almanach list-entities bca89ae64dba46b8b74653d8d9ae8364 2016-01-01 --end 2017-05-30

    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | Entity ID                            | Type     | Name   | Start                     | End  | Properties                                                                            |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d | instance | vm01   | 2017-05-09 14:19:14+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | f0690323-c394-4848-a272-964aad6431aa | instance | vm02   | 2017-05-15 18:31:42+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | 3e3b22e6-a10c-4c00-b8e5-05fcc8422b11 | volume   | vol01  | 2017-05-15 19:11:14+00:00 | None | {'size': 1, 'attached_to': [], 'volume_type': 'solidfire0'}                           |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+

Arguments:

* :code:`tenant_id`: Tenant ID (UUID)
* :code:`start`: Start date (ISO8601 format)
* :code:`end`: End date (ISO8601 format), optional

Get one Entity
--------------

Usage: :code:`almanach get-entity <entity_id>`

.. code:: bash

    almanach get-entity 3e3b22e6-a10c-4c00-b8e5-05fcc8422b11

    +----------------------------------+--------+------+---------------------------+------+-------------------------------------------------------------+
    | Tenant ID                        | Type   | Name | Start                     | End  | Properties                                                  |
    +----------------------------------+--------+------+---------------------------+------+-------------------------------------------------------------+
    | bca89ae64dba46b8b74653d8d9ae8364 | volume | vol1 | 2017-05-15 19:11:14+00:00 | None | {'size': 1, 'attached_to': [], 'volume_type': 'solidfire0'} |
    +----------------------------------+--------+------+---------------------------+------+-------------------------------------------------------------+

Arguments:

* :code:`entity_id`: Entity ID (UUID)

List Instances Entities
-----------------------

Usage: :code:`almanach list-instances <tenant_id> <start> <end>`

.. code:: bash

    almanach list-entities bca89ae64dba46b8b74653d8d9ae8364 2016-01-01 2017-05-30

    +--------------------------------------+--------+---------------------------+----------------------------------+---------+------------------------------------------------------------+
    | Instance ID                          | Name   | Start                     | End                              | Flavor  | Image Meta                                                 |
    +--------------------------------------+--------+---------------------------+----------------------------------+---------+------------------------------------------------------------+
    | f0690323-c394-4848-a272-964aad6431aa | vm02   | 2017-05-15 18:31:42+00:00 | None                             | A1.1    | {'distro': 'centos', 'version': '7', 'os_type': 'linux'}   |
    | 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d | vm01   | 2017-05-09 14:19:14+00:00 | 2017-05-17 09:37:47.775000+00:00 | A1.1    | {'distro': 'centos', 'version': '7', 'os_type': 'linux'}   |
    +--------------------------------------+--------+---------------------------+----------------------------------+---------+------------------------------------------------------------+

Arguments:

* :code:`tenant_id`: Tenant ID (UUID)
* :code:`start`: Start date (ISO8601 format)
* :code:`end`: End date (ISO8601 format)

Create Instance Entity
----------------------

Usage: :code:`almanach create_instance <tenant_id> <instance_id> <name> <flavor> <start> --image-meta <image_meta>`

Example:

.. code:: bash

    almanach create-instance bca89ae64dba46b8b74653d8d9ae8364 \
        8d8d0dc7-5f06-40aa-aba8-c4ff02aeb866 \
        my-instance \
        my-flavor \
        2017-01-01 \
        --image-meta '{"distro": "centos7", "type": "linux"}'

    Success

* :code:`tenant_id`: Tenant ID (UUID)
* :code:`instance_id`: Instance ID (UUID)
* :code:`start`: Start date (ISO8601 format)
* :code:`name`: Instance name (string)
* :code:`flavor`: Flavor (string)
* :code:`image_meta`: Image metadata (dict as JSON string)

Update Instance Entity
----------------------

Usage: :code:`almanach update-instance <instance_id> --start <start> --end <end> --name <name> --flavor <flavor>`

.. code:: bash

    almanach update-instance 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d --name vm03

    +-------------+----------------------------------------------------------+
    | Field       | Value                                                    |
    +-------------+----------------------------------------------------------+
    | Tenant ID   | bca89ae64dba46b8b74653d8d9ae8364                         |
    | Instance ID | 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d                     |
    | Start       | 2017-05-09 14:19:14+00:00                                |
    | End         | None                                                     |
    | Name        | vm03                                                     |
    | Flavor      | A1.1                                                     |
    | Image       | {'distro': 'centos', 'version': '7', 'os_type': 'linux'} |
    +-------------+----------------------------------------------------------+

Arguments:

* :code:`instance_id`: Instance ID (UUID)
* :code:`start`: Start date (ISO8601 format)
* :code:`end`: End date (ISO8601 format)
* :code:`name`: Instance name (string)
* :code:`flavor`: Flavor (string)

Delete Instance
---------------

Usage: :code:`almanach delete-instance <instance_id> --end <end>`

.. code:: bash

    almanach delete-instance 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d

    Success

Arguments:

* :code:`instance_id`: Instance ID (UUID)
* :code:`end`: End date (ISO8601 format), if not specified the current date time is used

Resize Instance
---------------

Usage: :code:`almanach resize-instance <instance_id> <flavor> --date <resize_date>`

.. code:: bash

    almanach resize-instance 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d New_Flavor

    Success

Arguments:

* :code:`instance_id`: Instance ID (UUID)
* :code:`flavor`: Flavor (string)
* :code:`date`: Resize date (ISO8601 format), if not specified the current datetime is used

List Volumes
------------

Usage: :code:`almanach list-volumes <tenant_id> <start> <end>`

.. code:: bash

    almanach list-volumes bca89ae64dba46b8b74653d8d9ae8364 2016-01-01 2017-09-01

    +--------------------------------------+------+---------------------------+------+------------+------+-------------+
    | Volume ID                            | Name | Start                     | End  | Type       | Size | Attachments |
    +--------------------------------------+------+---------------------------+------+------------+------+-------------+
    | 3e3b22e6-a10c-4c00-b8e5-05fcc8422b11 | vol1 | 2017-05-15 19:11:14+00:00 | None | solidfire0 |    1 | []          |
    +--------------------------------------+------+---------------------------+------+------------+------+-------------+

Arguments:

* :code:`tenant_id`: Tenant ID (UUID)
* :code:`start`: Start date (ISO8601 format)
* :code:`end`: End date (ISO8601 format)

Create Volume
-------------

Usage: :code:`almanach create-volume <tenant_id> <volume_id> <volume_type_id> <volume_name> <size> --date <creation_date> --attachment <instance_id>`

.. code:: bash

    almanach create-volume \
        8c3bc3aa-28d6-4863-b5ae-72e1b415f79d \
        3e3b22e6-a10c-4c00-b8e5-05fcc8422b11 \
        f3786e9f-f8e6-4944-a3bc-e11b9f112706 \
        my-volume \
        5 \
        --attachment=86dd5189-d9d6-40f7-a319-19231fbd4e07 \
        --attachment=252e49d8-abf2-486c-8478-b5f775134f54

    Success

Arguments:

* :code:`tenant_id`: Tenant ID (UUID)
* :code:`volume_id`: Volume ID (UUID)
* :code:`volume_type_id`: Volume ID (UUID)
* :code:`volume_name`: Volume name (string)
* :code:`size`: Volume size (integer)
* :code:`date`: Creation date (ISO8601 format), if not specified the current datetime is used
* :code:`attachment`: Attach the volume to one or many instances (UUID)

Delete Volume
-------------

Usage: :code:`almanach delete-volume <volume_id> --end <end>`

.. code:: bash

    almanach delete-volume 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d

    Success

Arguments:

* :code:`volume_id`: Instance ID (UUID)
* :code:`end`: End date (ISO8601 format), if not specified the current date time is used

Resize Volume
-------------

Usage: :code:`almanach resize-volume <volume_id> <size> --date <resize_date>`

.. code:: bash

    almanach resize-volume 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d 2

    Success

Arguments:

* :code:`volume_id`: Volume ID (UUID)
* :code:`size`: Volume size (integer)
* :code:`date`: Resize date (ISO8601 format), if not specified the current datetime is used

Attach Volume
-------------

Usage: :code:`almanach attach-volume <volume_id> --date <creation_date> --attachment <instance_id>`

.. code:: bash

    almanach attach-volume \
        8c3bc3aa-28d6-4863-b5ae-72e1b415f79d \
        --attachment=86dd5189-d9d6-40f7-a319-19231fbd4e07

    Success

Arguments:

* :code:`volume_id`: Volume ID (UUID)
* :code:`date`: Attachment date (ISO8601 format), if not specified the current datetime is used
* :code:`attachment`: Attach the volume to one or many instances (UUID)


Detach Volume
-------------

Usage: :code:`almanach detach-volume <volume_id> --date <creation_date> --attachment <instance_id>`

.. code:: bash

    almanach detach-volume \
        8c3bc3aa-28d6-4863-b5ae-72e1b415f79d \
        --attachment=86dd5189-d9d6-40f7-a319-19231fbd4e07

    Success

Arguments:

* :code:`volume_id`: Volume ID (UUID)
* :code:`date`: Attachment date (ISO8601 format), if not specified the current datetime is used
* :code:`attachment`: Attach the volume to one or many instances (UUID)

List Volume Types
-----------------

Usage: :code:`almanach list-volume-types`

.. code:: bash

    almanach list-volume-types

    +--------------------------------------+------------------+
    | Volume Type ID                       | Volume Type Name |
    +--------------------------------------+------------------+
    | f3786e9f-f8e6-4944-a3bc-e11b9f112706 | solidfire0       |
    +--------------------------------------+------------------+

Get Volume Type
---------------

Usage: :code:`almanach get-volume-type <volume_type_id>`

.. code:: bash

    almanach get-volume-type f3786e9f-f8e6-4944-a3bc-e11b9f112706

    +------------------+--------------------------------------+
    | Field            | Value                                |
    +------------------+--------------------------------------+
    | Volume Type ID   | f3786e9f-f8e6-4944-a3bc-e11b9f112706 |
    | Volume Type Name | solidfire0                           |
    +------------------+--------------------------------------+

Create Volume Type
------------------

Usage: :code:`almanach create-volume-type <volume_type_id> <volume_type_name>`

.. code:: bash

    almanach create-volume-type f1c2db7b-946e-47a4-b443-914a669a6672 my_volume_type

    Success

Delete Volume Type
------------------

Usage: :code:`almanach delete-volume-type <volume_type_id>`

.. code:: bash

    almanach delete-volume-type f1c2db7b-946e-47a4-b443-914a669a6672

    Success
