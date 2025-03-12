.. |logo| image:: https://beeware.org/project/toga/toga.png
    :width: 72px
    :target: https://beeware.org/toga

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Python Versions

.. |version| image:: https://img.shields.io/pypi/v/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Project version

.. |maturity| image:: https://img.shields.io/pypi/status/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Project status

.. |license| image:: https://img.shields.io/pypi/l/toga.svg
    :target: https://github.com/beeware/toga/blob/main/LICENSE
    :alt: BSD License

.. |ci| image:: https://github.com/beeware/toga/workflows/CI/badge.svg?branch=main
   :target: https://github.com/beeware/toga/actions
   :alt: Build Status

.. |social| image:: https://img.shields.io/discord/836455665257021440?label=Discord%20Chat&logo=discord&style=plastic
   :target: https://beeware.org/bee/chat/
   :alt: Discord server

|logo|

Toga
====

|pyversions| |version| |maturity| |license| |ci| |social|

A Python native, OS native GUI toolkit.

Minimum requirements
--------------------

* Toga requires **Python 3.9 or higher**.

* If you're on macOS, you need to be on 11 (Big Sur) or newer.

* If you're on Windows, you'll need Windows 10 or newer. If you are using
  Windows 10 and want to use a WebView to display web content, you will also
  need to install the `Edge WebView2 Evergreen Runtime
  <https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section>`__.
  Windows 11 has this runtime installed by default.

* If you're on Linux (or another Unix-based operating system), you need to have
  GTK+ >= 3.24 and glib >= 2.64. These are available starting with Ubuntu 20.04 and
  Fedora 32. You also need to install the system packages listed in `Linux platform
  documentation <https://toga.readthedocs.io/en/latest/reference/platforms/linux.html#prerequisites>`__.

Quickstart
----------

To get a demonstration of the capabilities of Toga, run the following::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window with some sample widgets.

Documentation
-------------

Documentation for Toga can be found on `Read The Docs`_.

.. _Read The Docs: https://toga.readthedocs.io

Financial support
-----------------

The BeeWare project would not be possible without the generous support of our financial
members:

.. image:: https://beeware.org/community/members/anaconda/anaconda-large.png
    :target: https://anaconda.com/
    :alt: Anaconda logo

Anaconda Inc. - Advancing AI through open source.

Plus individual contributions from `users like you
<https://beeware.org/community/members/>`__. If you find Toga, or other BeeWare tools
useful, please consider becoming a financial member.

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@beeware@fosstodon.org on Mastodon`_
* `Discord`_
* The Toga `Github Discussions forum`_

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

.. _BeeWare suite: https://beeware.org
.. _@beeware@fosstodon.org on Mastodon: https://fosstodon.org/@beeware
.. _Discord: https://beeware.org/bee/chat/
.. _Github Discussions forum: https://github.com/beeware/toga/discussions
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/

Contributing
------------

If you'd like to contribute to Toga development, our `guide for first time
contributors`_ will help you get started.

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.

.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute/index.html
.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
