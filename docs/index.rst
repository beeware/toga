Toga
====

A Python native, OS native GUI toolkit.

Quickstart
----------

In your virtualenv, install Toga, and then run it::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window showing the full range of widgets available
to an application using Toga.

Problems using virtualenv under Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toga uses the system native python GTK+3 bindings for display purposes.
However, if you're using a `--no-site-packages` virtualenv, the Python bindings
for GTK won't be in your `PYTHONPATH`.

Unfortunately, you can't `pip install` GTK+ bindings, so you have to use a
workaround. To make the system GTK+ bindings available to your virtualenv,
symlinking the `gi` module from the system dist-packages directory into your
virtualenv's site-packages::

    $ cd <your virtualenv dir>/lib/python2.7/site-packages
    $ ln -si /usr/lib/python2.7/dist-packages/gi

Documentation
-------------

Documentation for Toga can be found on `Read The Docs`_.

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

 * The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://toga.readthedocs.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers

Contents:

.. toctree::
   :maxdepth: 2
   :glob:

   introduction/philosophy
   introduction/tutorial-0

   reference/core
   reference/desktop
   reference/mobile

   internals/contributing
   internals/roadmap
   internals/releases
   internals/platforms/desktop/cocoa
   internals/platforms/desktop/gtk
   internals/platforms/desktop/win32
   internals/platforms/mobile/ios

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
