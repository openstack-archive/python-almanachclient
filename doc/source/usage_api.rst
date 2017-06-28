Almanach Python API
===================

.. module:: almanachclient
    :synopsis: A python client for the Almanach API.

.. currentmodule:: almanachclient

Usage
-----

First, create an Almanach Client instance by providing a Keystone session and your AUTH_TOKEN::

    >>> from keystoneauth1 import loading
    >>> from keystoneauth1 import session
    >>> from almanachclient.v1.client import Client

    >>> loader = loading.get_plugin_loader('password')
    >>> auth = loader.load_from_options(auth_url=AUTH_URL,
    ...                                 username=USERNAME,
    ...                                 password=PASSWORD,
    ...                                 project_name=PROJECT_NAME,
    ...                                 project_domain_name="Default",
    ...                                 user_domain_name="Default")
    >>> sess = session.Session(auth=auth)

    >>> almanach = Client(session=sess, token=AUTH_TOKEN)

Here ``ALMANACH_URL`` will be a string that represents the url of Almanach API.
``AUTH_TOKEN`` will be the authorization token you use to access the API.


You can also create a Keystone Client instance to fetch Almanach API endpoint::

    >>> from almanachclient.keystone_client import KeystoneClient
    >>> keystone_client = KeystoneClient(KEYSTONE_URL, USERNAME, PASSWORD, SERVICE, REGION)
    >>> almanach_url = keystone_client.get_endpoint_url()

In this case ``KEYSTONE_URL`` will be a string that represents the url of your keystone catalog.
The nature of ``USERNAME`` and ``PASSWORD`` speak for themselves. ``SERVICE`` will be a string
you use to identify the "almanach" service. ``REGION`` is used to determine which region the
"almanach" service is being used in.


Examples
--------

>>> import datetime
>>> from almanachclient.v1.client import Client

>>> start_date = datetime.datetime(2017, 01, 05)
>>> end_date = datetime.datetime(2017, 02, 05)

>>> almanach = Client('http://api.region.example.org', 'myApiAuthorizationToken')
>>> almanach.get_info()

>>> almanach.get_volume_types()
>>> almanach.get_volume_type('f1c2db7b-946e-47a4-b443-914a669a6673')
>>> almanach.create_volume_type('f1c2db7b-946e-47a4-b443-914a669a5555', 'VolumeTypeName')
>>> almanach.delete_volume_type('f1c2db7b-946e-47a4-b443-914a669a5555')

>>> almanach.get_tenant_entities('my-tenant-uuid', start_date, end_date)

>>> almanach.delete_instance('f1c2db7b-946e-47a4-b443-914a669a3333')
>>> almanach.update_instance_entity(instance_id='f1c2db7b-946e-47a4-b443-914a669a2222', start=start_date, end=end_date)


Reference
---------

For more information, see the reference:

.. toctree::
    :maxdepth: 2

    api/autoindex
