Positron
========

This is an example of an Electron-style "web site as app" project.

It serves a static site from the ``src/positron/resources/webapp`` folder.

Getting started
---------------

To set up a development environment::

    $ python -m venv venv
    $ ./venv/bin/activate
    (venv) $ pip install briefcase

To run in development mode::

    (venv) $ briefcase dev

To run as a packaged app::

    (venv) $ briefcase run
