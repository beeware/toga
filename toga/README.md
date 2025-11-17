# toga

[![Python Versions](https://img.shields.io/pypi/pyversions/toga.svg)](https://pypi.python.org/pypi/toga)
[![BSD-3-Clause License](https://img.shields.io/pypi/l/toga.svg)](https://github.com/beeware/toga/blob/main/LICENSE)
[![Project status](https://img.shields.io/pypi/status/toga.svg)](https://pypi.python.org/pypi/toga)

A meta-package for installing the [Toga widget toolkit](https://beeware.org/toga).

This package installs the [toga-core](https://pypi.org/project/toga-core) library, plus a different Toga backend depending the platform where it is installed:

- [toga-cocoa](https://pypi.org/project/toga-cocoa) on macOS
- [toga-gtk](https://pypi.org/project/toga-gtk) on Linux and FreeBSD
- [toga-winforms](https://pypi.org/project/toga-winforms) on Windows
- [toga-iOS](https://pypi.org/project/toga-ios) on iOS
- [toga-android](https://pypi.org/project/toga-winforms) on Android
- [toga-web](https://pypi.org/project/toga-web) on Emscripten

Backends are also available for [Textual](https://pypi.org/project/toga-textual), [Qt](https://pypi.org/project/toga-qt), and for [testing](https://pypi.org/project/toga-dummy); however, these must be installed manually.

Some platforms have additional prerequisites; see the [Toga platform guide](https://toga.beeware.org/en/latest/reference/platforms/) for details.

For more details, see [Toga's documentation](https://toga.beeware.org), or the [Toga project on GitHub](https://github.com/beeware/toga).

# Community

Toga is part of the [BeeWare suite](https://beeware.org). You can talk to the community through:

- [@beeware@fosstodon.org on Mastodon](https://fosstodon.org/@beeware)
- [Discord](https://beeware.org/bee/chat/)
- The Toga [GitHub Discussions forum](https://github.com/beeware/toga/discussions)

We foster a welcoming and respectful community as described in our [BeeWare Community Code of Conduct](https://beeware.org/community/behavior/).

# Contributing

If you experience problems with Toga, [log them on GitHub](https://github.com/beeware/toga/issues).

If you'd like to contribute to Toga development, our [contribution guide](https://toga.beeware.org/en/latest/how-to/contribute/) details how to set up a development environment, and other requirements we have as part of our contribution process.
