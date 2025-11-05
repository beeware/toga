# Linux/Unix (Qt)

The Toga backend for Linux (and other Unix-like operating systems) running KDE is [`toga-qt`](https://github.com/beeware/toga/tree/main/qt).

`toga-qt` requires Python 3.10+, and Qt 6.8 or newer.

/// warning | Experimental Backend

While the GTK 3 backend is mostly completed in functionality, the Qt backend is currently a pre-alpha prototype.

///

/// admonition | Qt on Windows and macOS

Although Qt *can* be installed on Windows and macOS, and the `toga-qt` backend *may* work on those platforms, this is not officially supported by Toga. We recommend using `toga-winforms` on [Windows][], and `toga-cocoa` on [macOS][].

///

## Prerequisites  { #qt-prerequisites }

Most Qt testing occurs with Qt 6.10 as this is the version that is installable through ``pip``'s PySide6.

The system packages that provide Qt must be installed manually:

-8<- "reference/platforms/qt-prerequisites.md"

## Installation

`toga-qt` must be manually installed along with ``toga-core`` if its usage is desired:

```console
$ python -m pip install toga-core[pyside6]
```

## Implementation Details

The `toga-qt` backend uses Qt 6.

The native APIs are accessed using the [PySide6 bindings](https://www.qt.io/development/qt-framework/python-bindings).
