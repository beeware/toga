===
Web
===

Toga is able to deploy apps as a single-page web app using the `toga-web
<https://github.com/beeware/toga/tree/main/web>`__ backend.

.. note::

    The Web backend is currently proof-of-concept only. Most widgets have not been
    implemented.

Prerequisites
-------------

``toga-web`` will run in any modern browser. It requires `PyScript`_ 2023.05.01 or
newer, and `Shoelace v2.3 <https://shoelace.style>`__.

Installation
------------

The recommended approach for deploying ``toga-web`` is to use `Briefcase
<https://briefcase.readthedocs.org>`__ to package your app.

``toga-web`` can be installed manually by adding ``toga-web`` to your ``pyscript.toml``
configuration file.

Implementation details
----------------------

``toga-web`` uses `PyScript`_ to run Python code in the browser.

.. _PyScript: https://pyscript.net
