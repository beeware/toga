Toga
====

A Python native, OS native GUI toolkit.

This package provides the core Toga API. In order to use Toga, you'll also need to
install a backend that implements the core Toga API for that platform:

* **Android** `toga-android <https://pypi.org/project/toga-android>`__
* **iOS** `toga-iOS <https://pypi.org/project/toga-iOS>`__
* **Linux** `toga-gtk <https://pypi.org/project/toga-gtk>`__
* **macOS** `toga-cocoa <https://pypi.org/project/toga-cocoa>`__
* **Web** `toga-web <https://pypi.org/project/toga-web>`__
* **Windows** `toga-winforms <https://pypi.org/project/toga-winforms>`__

Minimum requirements
--------------------

* Toga requires **Python 3.8** or newer. Python 2 is not supported.

* If you're on macOS, you need to be on 10.10 (Yosemite) or newer.

* If you're on Windows, you'll need Windows 10 or newer. If you are using
  Windows 10 and want to use a WebView to display web content, you will also
  need to install the `Edge WebView2 Evergreen
  Runtime. <https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section>`__
  Windows 11 has this runtime installed by default.

* If you're on Linux (or another Unix-based operating system), you need to have
  GTK+ 3.10 or newer. This is the version that ships starting with Ubuntu 14.04
  and Fedora 20. You also need to install the system packages listed
  in `Tutorial 0 <docs/tutorial/tutorial-0.rst>`__.

* If you're on Android, you'll need Android SDK 24 (Android 7 / Nougat) or newer.

* If you're on iOS, you'll need iOS 11 or newer.

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

.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute-code.html
.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
