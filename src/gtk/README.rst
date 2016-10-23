toga-gtk
========

A GTK+ backend for the `Toga widget toolkit`_.

**Toga requires Python 3**

This package isn't much use by itself; it needs to be combined with `the core Toga library`_.

For more details, see the `Toga project on Github`_.

Prerequisites
~~~~~~~~~~~~~

This backend requires GTK+ 3.10 or later. This is the version that ships
starting with Ubuntu 14.04 and Fedora 20. You also need to install the Python
3 bindings to GTK+. If you want to use the WebView widget, you'll also need to
have WebKit, plus the GI bindings to WebKit installed. This means you'll need
to install the following:

* **Ubuntu 14.04** ``apt-get install python3-gi gir1.2-webkit2-3.0``

* **Ubuntu 16.04** ``apt-get install python3-gi gir1.2-webkit2-4.0``
  or ``apt-get install python3-gi gir1.2-webkit2-3.0``

* **Fedora 20+** ???

* **Debian** ???

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `pybee/general`_ channel on Gitter.

Contributing
------------

If you experience problems with this backend, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _Toga widget toolkit: http://pybee.org/toga
.. _the core Toga library: https://github.com/pybee/toga-core
.. _Toga project on Github: https://github.com/pybee/toga
.. _BeeWare suite: http://pybee.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _log them on Github: https://github.com/pybee/toga-gtk/issues
.. _fork the code: https://github.com/pybee/toga-gtk
.. _submit a pull request: https://github.com/pybee/toga-gtk/pulls
