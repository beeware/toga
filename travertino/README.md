# Travertino

[![Python Versions](https://img.shields.io/pypi/pyversions/travertino.svg)](https://pypi.python.org/pypi/travertino)
[![BSD-3-Clause License](https://img.shields.io/pypi/l/travertino.svg)](https://github.com/beeware/toga/blob/main/travertino/LICENSE)
[![Project status](https://img.shields.io/pypi/status/travertino.svg)](https://pypi.python.org/pypi/travertino)

Travertino is a set of constants and utilities for describing user interfaces, including:

- colors
- directions
- text alignment
- sizes

# Usage

Install Travertino:

```console
$ pip install travertino
```

Then in your python code, import and use it:

```python
>>> from travertino.colors import color, rgb

# Define a new color as an RGB triple
>>> red = rgb(0xff, 0x00, 0x00)

# Parse a color from a string
>>> Color.parse('#dead00')
rgb(0xde, 0xad, 0x00)

# Reference a pre-defined color
>>> Color.parse('RebeccaPurple')
rgb(102, 51, 153)
```

## Community

Travertino is part of the [BeeWare suite](https://beeware.org). You can talk to the community through:

- [@beeware@fosstodon.org on Mastodon](https://fosstodon.org/@beeware)
- [Discord](https://beeware.org/bee/chat/)

We foster a welcoming and respectful community as described in our [BeeWare Community Code of Conduct](https://beeware.org/community/behavior/).

## Contributing

If you experience problems with Toga, [log them on GitHub](https://github.com/beeware/toga/issues).

If you'd like to contribute to Toga development, our [contribution guide](https://toga.beeware.org/en/latest/how-to/contribute/) details how to set up a development environment, and other requirements we have as part of our contribution process.
