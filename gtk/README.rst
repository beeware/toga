toga-gtk
========

A GTK backend for the `Toga widget toolkit`_.

**Toga requires Python 3**

This package isn't much use by itself; it needs to be combined with `the core Toga library`_.

For more details, see the `Toga project on Github`_.

.. _Toga widget toolkit: http://beeware.org/toga
.. _the core Toga library: https://pypi.python.org/pypi/toga-core
.. _Toga project on Github: https://github.com/beeware/toga

Prerequisites
~~~~~~~~~~~~~

This backend requires GTK 3.10 or later. This is the version that ships
starting with Ubuntu 14.04 and Fedora 20. You also need to install the Python
3 bindings to GTK. If you want to use the WebView widget, you'll also need to
have WebKit, plus the GI bindings to WebKit installed. This means you'll need
to install the following:

* **Ubuntu 14.04** ``apt-get install python3-gi gir1.2-webkit-3.0``

* **Ubuntu 16.04 / Debian 8** ``apt-get install python3-gi gir1.2-webkit2-4.0``
  or ``apt-get install python3-gi gir1.2-webkit-3.0``

* **Fedora** ``dnf install python3-gobject pywebkitgtk``
  or ``yum install python3-gobject pywebkitgtk``

* **Arch Linux** ``pacman -S python-gobject webkit2gtk``

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
