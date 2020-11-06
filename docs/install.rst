Installation
============

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
