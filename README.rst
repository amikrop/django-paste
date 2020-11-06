django-paste
============

Pluggable, configurable, pastebin HTTP REST API
-----------------------------------------------

.. image:: https://img.shields.io/pypi/v/django-paste.svg
   :target: https://pypi.org/project/django-paste/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/django-paste.svg
   :target: https://pypi.org/project/django-paste/
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/django-paste.svg
   :target: https://pypi.org/project/django-paste/
   :alt: PyPI - Python Version

.. image:: https://codecov.io/gh/amikrop/django-paste/branch/master/graph/
           badge.svg
    :target: https://codecov.io/gh/amikrop/django-paste/
    :alt: Coverage

.. image:: https://travis-ci.org/amikrop/django-paste.svg?branch=master
   :target: https://travis-ci.org/amikrop/django-paste/
   :alt: Build Status

.. image:: https://readthedocs.org/projects/django-paste/badge/?version=latest
   :target: https://django-paste.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

*django-paste* is a simple `Django <https://www.djangoproject.com/>`_
pluggable app of a code pasting and highlighting HTTP REST API, written using
`Django REST framework <https://www.django-rest-framework.org/>`_. It supports
the `CRUD <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_
operations on source code snippets and uses any existing user authentication
system. Syntax highlighting is powered by `Pygments
<https://pygments.org/>`_.

Installation
------------

The following Python versions are supported:

    - CPython: 3.6, 3.7, 3.8, 3.9
    - PyPy: 3.6

Django:

    - 2.0, 2.1, 2.2
    - 3.0, 3.1

- Install via `pip
  <https://packaging.python.org/tutorials/installing-packages/>`_:

  .. code-block:: bash

     $ pip install django-paste

- Add it to your ``INSTALLED_APPS``:

  .. code-block:: python

     INSTALLED_APPS = [
         # ...
         'paste.apps.PasteConfig',
     ]

- Register the app's URLs under a path of your choice:

  .. code-block:: python

     urlpatterns = [
         # ...
         path('some-path/', include('paste.urls')),
     ]

  where ``'some-path/'`` could be any URL.

- Optionally, configure the app `settings
  <https://django-paste.readthedocs.io/en/latest/settings.html>`_.

- Generate and run the database migrations:

  .. code-block:: bash

     $ python manage.py makemigrations paste
     $ python manage.py migrate

Usage
-----

You can find the description of the app's `endpoints
<https://django-paste.readthedocs.io/en/latest/api.html#endpoints>`_ and
snippet `fields <https://django-paste.readthedocs.io/en/latest/fields.html>`_
in the `documentation <https://django-paste.readthedocs.io/en/latest/>`_. You
can also manage snippets at the Django admin site.

License
-------

Distributed under the `MIT License
<https://github.com/amikrop/django-paste/blob/master/LICENSE>`_.
