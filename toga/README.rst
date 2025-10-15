.. |pyversions| image:: https://img.shields.io/pypi/pyversions/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Python Versions

.. |license| image:: https://img.shields.io/pypi/l/toga.svg
    :target: https://github.com/beeware/toga/blob/main/LICENSE
    :alt: BSD-3-Clause License

.. |maturity| image:: https://img.shields.io/pypi/status/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Project status

toga
====

|pyversions| |license| |maturity|

A meta-package for installing the `Toga widget toolkit`_.

This package installs the `toga-core <https://pypi.org/project/toga-core>`__ library,
plus a different Toga backend depending the platform where it is installed:

* `toga-cocoa <https://pypi.org/project/toga-cocoa>`__ on macOS
* `toga-gtk <https://pypi.org/project/toga-gtk>`__ on Linux and FreeBSD
* `toga-winforms <https://pypi.org/project/toga-winforms>`__ on Windows

Backends are also available for `Android <https://pypi.org/project/toga-android>`__,
`iOS <https://pypi.org/project/toga-iOS>`__, `single-page web apps
<https://pypi.org/project/toga-web>`__, and `testing
<https://pypi.org/project/toga-dummy>`__; however, these must be installed manually.

Some platforms have additional prerequisites; see the `Toga platform guide
<https://toga.readthedocs.io/en/latest/reference/platforms/>`__ for details.

For more details, see the `Toga project on GitHub`_.

.. _Toga widget toolkit: https://beeware.org/toga
.. _Toga project on GitHub: https://github.com/beeware/toga

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@beeware@fosstodon.org on Mastodon`_
* `Discord`_
* The Toga `GitHub Discussions forum`_

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

.. _BeeWare suite: https://beeware.org
.. _@beeware@fosstodon.org on Mastodon: https://fosstodon.org/@beeware
.. _Discord: https://beeware.org/bee/chat/
.. _GitHub Discussions forum: https://github.com/beeware/toga/discussions
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/

Contributing
------------

If you experience problems with Toga, `log them on GitHub
<https://github.com/beeware/toga/issues>`__.

If you'd like to contribute to Toga development, our `contribution guide
<https://toga.readthedocs.io/en/latest/how-to/contribute/>`__
details how to set up a development environment, and other requirements we have
as part of our contribution process.
