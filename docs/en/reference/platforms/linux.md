# Linux/Unix

![image](../images/gtk.png){ width="300px" }

/// caption

///

<!-- TODO: Update alt text -->

The Toga backend for Linux (and other Unix-like operating systems) is [`toga-gtk`](https://github.com/beeware/toga/tree/main/gtk) for
GNOME-based Desktops or [`toga-qt`](https://github.com/beeware/toga/tree/main/qt) for KDE-based desktops.

/// admonition | Qt support

The Qt backend is relatively new, and most widgets are missing.  To get started on
contributing, refer to our [Contributing Code to Toga](/how-to/contribute/code.md) guide.

///

/// admonition | GTK and/or Qt on Windows and macOS

Although GTK or Qt *can* be installed on Windows and macOS, and the `toga-gtk` and `toga-qt` backends *may* work on those platforms, this is not officially supported by Toga. We recommend using `toga-winforms` on [Windows][], and `toga-cocoa` on [macOS][].

///

## Prerequisites  { #linux-prerequisites }

`toga-gtk` requires Python 3.10+, and GTK 3.22 or newer.  `toga-qt` requires Python 3.10+, and Qt 6.8 or newer.

Most GTK testing occurs with GTK 3.24 as this is the version that has shipped with all versions of Ubuntu since Ubuntu 20.04, and all versions of Fedora since Fedora 32.

Most Qt testing occurs with Qt 6.10 as this is the version that is installable through ``pip``'s PySide6 which we must use since Ubuntu 24.04 does not yet provide PySide6 through the system.

The system packages that provide GTK or Qt must be installed manually:

-8<- "reference/platforms/unix-prerequisites.md"

Toga does not currently support GTK 4.

## Installation

`toga-gtk` is installed automatically on any Linux machine (machines that report `sys.platform == 'linux'`), or any FreeBSD machine (machines that report `sys.platform == 'freebsd*'`). It can be manually installed by running:

```console
$ python -m pip install toga-gtk
```

`toga-qt` must be manually installed along with ``toga-core`` if its usage is desired:

```console
$ python -m pip install toga-core[system]
```

Or, if your distribution does not provide system PySide6 packages:

```console
$ python -m pip install toga-core[pyside6]
```

## Implementation details

The `toga-gtk` backend uses the [GTK3 API](https://docs.gtk.org/gtk3/).

The native APIs are accessed using the [PyGObject binding](https://pygobject.readthedocs.io).

The `toga-qt` backend uses Qt 6.

The native APIs are accessed using the [PySide6 bindings](https://www.qt.io/development/qt-framework/python-bindings).
