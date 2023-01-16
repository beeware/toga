Positron
========

This is an example of an Electron-style "web site as app" project.

It serves a Django site called ``webapp``, contained in ``src/webapp``. The
contents of this folder are a stock version of what is produced by
``django-admin.py startproject``, collapsed into a single directory.

Getting started
---------------

To set up a development environment::

    $ python -m venv venv
    $ ./venv/bin/activate
    (venv) $ pip install briefcase

To run Django management commands::

    PYTHONPATH=src python src/webapp/manage.py

To run in development mode::

    (venv) $ briefcase dev

To run as a packaged app::

    (venv) $ briefcase run
