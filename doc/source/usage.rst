Command Line Usage
==================

Environment variables
---------------------

* `OS_AUTH_URL`: Keystone URL (v3 endpoint)
* `OS_AUTH_URL`: OpenStack region name
* `OS_USERNAME`: OpenStack username
* `OS_PASSWORD`: OpenStack password
* `ALMANACH_SERVICE`: Almanach catalog service name
* `ALMANACH_TOKEN`: Almanach private key

Get server version
------------------

.. code:: bash

    almanach-client version

    4.0.9

Get Endpoint URL
----------------

.. code:: bash

    almanach-client endpoint

    http://almanach.example.org

Get tenant entities
-------------------

.. code:: bash

    almanach-client tenant entities bca89ae64dba46b8b74653d8d9ae8364 2016-01-01 2017-05-30

    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | Entity ID                            | Type     | Name   | Start                     | End  | Properties                                                                            |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
    | 8c3bc3aa-28d6-4863-b5ae-72e1b415f79d | instance | vm01   | 2017-05-09 14:19:14+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | f0690323-c394-4848-a272-964aad6431aa | instance | vm02   | 2017-05-15 18:31:42+00:00 | None | {'image': {'distro': 'centos', 'version': '7', 'os_type': 'linux'}, 'flavor': 'A1.1'} |
    | 3e3b22e6-a10c-4c00-b8e5-05fcc8422b11 | volume   | vol01  | 2017-05-15 19:11:14+00:00 | None | {'attached_to': [], 'volume_type': 'solidfire0'}                                      |
    +--------------------------------------+----------+--------+---------------------------+------+---------------------------------------------------------------------------------------+
