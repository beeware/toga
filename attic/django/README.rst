toga-django
===========

A `Django <https://djangoproject.com>`__ backend for the `Toga widget toolkit`_.

This package isn't much use by itself; it needs to be combined with `the core
Toga library`_ and `the Toga Web library`_.

For more details, see the `Toga project on Github`_.

.. _Toga widget toolkit: http://beeware.org/toga
.. _the core Toga library: https://pypi.python.org/pypi/toga-core
.. _the Toga Web library: https://pypi.python.org/pypi/toga-web
.. _Toga project on Github: https://github.com/beeware/toga

Prerequisites
~~~~~~~~~~~~~

This backend requires Django 3.0 as a minimum requirement.

Usage
~~~~~

Toga Django defines a ``TogaApp`` class that can be used to mount a Toga Web
instance in a Django app. If you have Toga application named `myapp`, Django
deployment is achieved by putting the following into your project's
``urls.py``::

    from django.conf import settings
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.urls import path

    from toga_django import TogaApp

    from tutorial import app

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('/', TogaApp(app).urls),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

This will mount the Toga app at `/`, the Django admin at `/admin`, and serve
static content in debug mode. You can mount the app at any URL you wish,
and you can also add other routes for other views.

The app can then be executed with::

    $ ./manage.py runserver

This assumes a standard Toga app layout, where the application `myapp` has a
submodule `app.py` that defines a `main()` method.

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@beeware@fosstodon.org on Mastodon`_
* `Discord`_
* The Toga `Github Discussions forum`_

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

.. _BeeWare suite: http://beeware.org
.. _@beeware@fosstodon.org on Mastodon: https://fosstodon.org/@beeware
.. _Discord: https://beeware.org/bee/chat/
.. _Github Discussions forum: https://github.com/beeware/toga/discussions
.. _BeeWare Community Code of Conduct: http://beeware.org/community/behavior/

Contributing
------------

If you experience problems with this backend, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
