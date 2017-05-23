The :mod:`almanachclient` Python API
====================================

.. module:: almanachclient
:synopsis: A python client for the Almanach API.

Usage
-----

First, create an Almanach Client instance with your credentials::

    >>> from almanachclient.v1.client import Client
    >>> almanach = Client(URL, AUTH_TOKEN)

Here ``URL`` will be a string that represents the url of your API.
``AUTH_TOKEN`` will be the authorization token you use to acces the API.


You can also create a Keystone Client instance and access the API with it::

    >>> from almanachclient.keystone_client import KeystoneClient
    >>> keystone_client = KeystoneClient(KEYSTONE_URL, USERNAME, PASSWORD, SERVICE, REGION)
    >>> keystone_client.get_endpoint_url('admin')

In this case ``KEYSTONE_URL`` will be a string that represents the url of your keystone catalog.
The nature of ``USERNAME`` and ``PASSWORD`` speak for themselves. ``SERVICE`` will be a string
you use to identify the "almanach" service. ``REGION`` is used to determine which region the
"almanach" service is being used in.


Examples
--------
>>> import datetime
>>> from almanachclient.v1.client import Client

>>> start_date = datetime.datetime(2017,01,05)
>>> end_date = datetime.datetime(2017,02,05)

>>> almanach = Client('http://api.region.example.org',  'myApiAuthorizationToken')
>>> almanach.get_info()

>>> almanach.get_volume_types()
>>> almanach.get_volume_type('f1c2db7b-946e-47a4-b443-914a669a6673')
>>> almanach.create_volume_type('f1c2db7b-946e-47a4-b443-914a669a5555', 'VolumeTypeName')
>>> almanach.delete_volume_type('f1c2db7b-946e-47a4-b443-914a669a5555')

>>> almanach.get_tenant_entities('my-tenant-uuid', start_date, end_date)

>>> almanach.delete_instance('f1c2db7b-946e-47a4-b443-914a669a3333')
>>> almanach.update_instance_entity(instance_id='f1c2db7b-946e-47a4-b443-914a669a2222', start=start_date, end=end_date)
