toga-gtk
========

A GTK+ backend for the `Toga widget toolkit`_.

This package isn't much use by itself; it needs to be combined with `the core Toga library`_.

For more details, see the `Toga project on Github`_.

Prerequisites
~~~~~~~~~~~~~

This backend requires GTK+ 3.4 as a minimum. This is the version provided
out of the box by Ubunutu 12.04.

If you want to use a WebView, you'll also need to have WebKit, plus the
GI bindings to WebKit (gir1.2-webkit-3.0) installed.

Problems using virtualenv under Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running under Linux, toga-gtk uses the system native python GTK+3
bindings for display purposes. However, if you're using a `--no-site-packages`
virtualenv, the Python bindings for GTK won't be in your `PYTHONPATH`.

Unfortunately, you can't `pip install` GTK+ bindings, so you have to use a
workaround. To make the system GTK+ bindings available to your virtualenv,
symlinking the `gi` module from the system dist-packages directory into your
virtualenv's site-packages::

    $ cd $VIRTUAL_ENV/lib/python2.7/site-packages
    $ ln -si /usr/lib/python2.7/dist-packages/gi

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

* The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

Contributing
------------

If you experience problems with this backend, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _Toga widget toolkit: http://pybee.org/toga
.. _the core Toga library: https://github.com/pybee/toga
.. _Toga project on Github: https://github.com/pybee/toga
.. _BeeWare suite: http://pybee.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers
.. _log them on Github: https://github.com/pybee/toga-gtk/issues
.. _fork the code: https://github.com/pybee/toga-gtk
.. _submit a pull request: https://github.com/pybee/toga-gtk/pulls
