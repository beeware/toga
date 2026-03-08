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

Most Qt testing occurs with Qt 6.10 as this is the version that is installable through `pip`.

The system packages that provide Qt must be installed manually:

-8<- "snippets/qt-prerequisites.md"

## Installation

`toga-qt` must be installed directly using `pip`. The `pyside6` optional extra is used to request the installation of the Python language bindings for Qt.

```console
$ python -m pip install toga-qt[pyside6]
```

This will install the full `PySide6` package, which includes both `PySide6-Essentials` and `PySide6-Addons`. The `PySide6-Addons` package is required to support the [WebView][] widget. If your app does not use [WebView][], you can specify a requirement of `toga-qt[pyside6-essentials]` to only install the `PySide6-Essentials` package.

## Implementation Details

The `toga-qt` backend uses Qt 6.

The native APIs are accessed using the [PySide6 bindings](https://www.qt.io/development/qt-framework/python-bindings).

## Using System Qt

If you want to use the system Qt runtime installed through your system package manager (which provides better integration with system-provided themes), you can install `toga-qt` with the `system` extra:

```console
$ python -m pip install toga-qt[system]
```

This installs `system-pyside6`, which allows using the system-provided PySide6 runtime. Since PySide6 bindings are static and specific to one version of Qt, they need to be provided through the system package manager to use the system Qt runtime. This approach enables integration with system-provided themes.

To use this option, you must also install the PySide6 system packages. The PySide6 system packages, with minimum distribution versions, may be found in the [system-pyside6 README](https://github.com/beeware/system-pyside6).
