Command Line Usage
==================

Environment variables
---------------------

* :code:`OS_AUTH_URL`: Keystone URL (v3 endpoint)
* :code:`OS_AUTH_URL`: OpenStack region name
* :code:`OS_USERNAME`: OpenStack username
* :code:`OS_PASSWORD`: OpenStack password
* :code:`ALMANACH_SERVICE`: Almanach catalog service name
* :code:`ALMANACH_TOKEN`: Almanach API key

Get server version
------------------

Usage: :code:`almanach-client version`

.. code:: bash

    almanach-client version

    4.0.9

Get Endpoint URL
----------------

Usage: :code:`almanach-client endpoint`

.. code:: bash

    almanach-client endpoint

    http://almanach.example.org

Get tenant entities
-------------------

Usage: :code:`almanach-client list-entities <tenant_id> <start> <end>`

.. code:: bash

    almanach-client list-entities bca89ae64dba46b8b74653d8d9ae8364 2016-01-01 2017-05-30

    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | Entity ID                            | Type     | Name   | Start                     | End  | Properties                                                                            |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d | instance | vm01   | 2017-05-09 14:19:14+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | f0690323-c394-4848-a272-964aad6431aa | instance | vm02   | 2017-05-15 18:31:42+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | 3e3b22e6-a10c-4c00-b8e5-05fcc8422b11 | volume   | vol01  | 2017-05-15 19:11:14+00:00 | None | {'attached_to': [], 'volume_type': 'solidfire0'}                                      |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+

Update Instance Entity
----------------------

Usage: :code:`almanach-client update-instance <instance_id> --start <start> --end <end> --name <name> --flavor <flavor>`

.. code:: bash

    almanach-client update-instance 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d --name vm03

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

List Volume Types
-----------------

Usage: :code:`almanach-client list-volume-types`

.. code:: bash

    almanach-client list-volume-types

    +--------------------------------------+------------------+
    | Volume Type ID                       | Volume Type Name |
    +--------------------------------------+------------------+
    | f3786e9f-f8e6-4944-a3bc-e11b9f112706 | solidfire0       |
    +--------------------------------------+------------------+

Get Volume Type
---------------

Usage: :code:`almanach-client get-volume-type <volume_type_id>`

.. code:: bash

    almanach-client get-volume-type f3786e9f-f8e6-4944-a3bc-e11b9f112706

    +------------------+--------------------------------------+
    | Field            | Value                                |
    +------------------+--------------------------------------+
    | Volume Type ID   | f3786e9f-f8e6-4944-a3bc-e11b9f112706 |
    | Volume Type Name | solidfire0                           |
    +------------------+--------------------------------------+

Create Volume Type
------------------

Usage: :code:`almanach-client create-volume-type <volume_type_id> <volume_type_name>`

.. code:: bash

    almanach-client create-volume-type f1c2db7b-946e-47a4-b443-914a669a6672 my_volume_type

    Success

Delete Volume Type
------------------

Usage: :code:`almanach-client delete-volume-type <volume_type_id>`

.. code:: bash

    almanach-client delete-volume-type f1c2db7b-946e-47a4-b443-914a669a6672

    Success
