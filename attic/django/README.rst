toga-django
===========

A `Django <https://djangoproject.com>`__ backend for the `Toga widget toolkit
<https://beeware.org/toga>`__.

This package isn't much use by itself; it needs to be combined with `the core
Toga library <https://pypi.python.org/pypi/toga-core>`__ and `the Toga Web
library <https://pypi.python.org/pypi/toga-web>`__.

For more details, see the `Toga project on Github
<https://github.com/beeware/toga>`__.

Prerequisites
~~~~~~~~~~~~~

This backend requires Django 3.0 as a minimum requirement.

Usage
~~~~~

Toga Django defines a ``TogaApp`` class that can be used to mount a Toga Web
instance in a Django app. If you have Toga application named `myapp`, Django
deployment is acheived by putting the following into your project's
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

Toga is part of the `BeeWare suite <http://beeware.org>`__. You can talk to the
community through:

* `@pybeeware on Twitter <https://twitter.com/pybeeware>`__

* `Discord <https://beeware.org/bee/chat/>`__

* The Toga `Github Discussions forum <https://github.com/beeware/toga/discussions>`__

Contributing
------------

If you experience problems with this backend, `log them on GitHub
<https://github.com/beeware/toga/issues>`_. If you want to contribute code,
please `fork the code <https://github.com/beeware/toga>`__ and `submit a pull
request <https://github.com/beeware/toga/pulls>`_.
