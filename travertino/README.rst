.. |pyversions| image:: https://img.shields.io/pypi/pyversions/travertino.svg
    :target: https://pypi.python.org/pypi/travertino
    :alt: Python Versions

.. |license| image:: https://img.shields.io/pypi/l/travertino.svg
    :target: https://github.com/beeware/toga/blob/main/travertino/LICENSE
    :alt: BSD-3-Clause License

.. |maturity| image:: https://img.shields.io/pypi/status/travertino.svg
    :target: https://pypi.python.org/pypi/travertino
    :alt: Project status

Travertino
==========

|pyversions| |license| |maturity|

Travertino is a set of constants and utilities for describing user
interfaces, including:

* colors
* directions
* text alignment
* sizes

Usage
-----

Install Travertino:

    $ pip install travertino

Then in your python code, import and use it::

    >>> from travertino.colors import color, rgb

    # Define a new color as an RGB triple
    >>> red = rgb(0xff, 0x00, 0x00)

    # Parse a color from a string
    >>> color('#dead00')
    rgb(0xde, 0xad, 0x00)

    # Reference a pre-defined color
    >>> color('RebeccaPurple')
    rgb(102, 51, 153)


Community
---------

Travertino is part of the `BeeWare suite <https://beeware.org>`_. You can talk to the
community through:

* `@beeware@fosstodon.org on Mastodon <https://fosstodon.org/@beeware>`__

* `Discord <https://beeware.org/bee/chat/>`__

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct <https://beeware.org/community/behavior/>`__.

Contributing
------------

If you experience problems with Toga, `log them on GitHub
<https://github.com/beeware/toga/issues>`__.

If you'd like to contribute to Toga development, our `contribution guide
<https://toga.readthedocs.io/en/latest/how-to/contribute/>`__
details how to set up a development environment, and other requirements we have
as part of our contribution process.
