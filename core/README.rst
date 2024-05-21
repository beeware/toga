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

Toga requires **Python 3.8** or newer. Python 2 is not supported.

Each backend also has specific requirements and pre-requisites. See the `platform
documentation <https://toga.readthedocs.io/en/latest/reference/platforms.html>`__ for
details.

Quickstart
----------

To get a demonstration of the capabilities of Toga, run the following::

    $ python -m pip install toga-demo
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

.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute/index.html
.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
