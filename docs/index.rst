====
Toga
====

Toga is a Python native, OS native, cross platform GUI toolkit.

Quickstart
==========

In your virtualenv, install Toga, and then run it::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window showing the full range of widgets available
to an application using Toga.

Prerequisites
~~~~~~~~~~~~~

Toga has some minimum requirements:

* If you're on OS X, you need to be on 10.7 (Lion) or newer.

* If you're on Linux, you need to have GTK+ 3.4 or later. This is the
  version that ships with Ubuntu 12.04; you'll need to have the
  ``python3-gi`` package installed. If you want to use the WebView widget,
  you'll also need to have WebKit, plus the GI bindings to WebKit
  (``gir1.2-webkit-3.0``) installed.

If these requirements aren't met, Toga either won't work at all, or won't
have full functionality.

Community
=========

Toga is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

 * The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://toga.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers

Contents
========

.. toctree::
   :maxdepth: 2
   :glob:

   philosophy
   tutorial/index
   reference/index
   internals/index
