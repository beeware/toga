<!-- rumdl-disable-line MD041 -->

/// tab | GTK

These instructions are different on almost every version of Linux and Unix; here are some of the common alternatives:

### Ubuntu 24.04+ / Debian 13+

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git build-essential pkg-config python3-dev libgirepository-2.0-dev libcairo2-dev gir1.2-gtk-3.0 libcanberra-gtk3-module
```

### Ubuntu 22.04 / Debian 11, 12

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git build-essential pkg-config python3-dev libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0 libcanberra-gtk3-module
```

If you're running on Ubuntu 22.04, Debian 11 or Debian 12, you'll also need to add a pin for `PyGObject==3.50.0`. Later versions of PyGObject require the `libgirepository-2.0-dev` library, which isn't available on older Debian-based distributions.

### Fedora 41+

```console
(venv) $ sudo dnf install git gcc make pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel gtk3 libcanberra-gtk3
```

### Arch / Manjaro

```console
(venv) $ sudo pacman -Syu git base-devel pkgconf python3 gobject-introspection cairo gtk3 libcanberra
```

### OpenSUSE Tumbleweed

```console
(venv) $ sudo zypper install git patterns-devel-base-devel_basis pkgconf-pkg-config python3-devel gobject-introspection-devel cairo-devel gtk3 'typelib(Gtk)=3.0' libcanberra-gtk3-module
```

### FreeBSD

```console
(venv) $ sudo pkg update
(venv) $ sudo pkg install git gcc cmake pkgconf python3 gobject-introspection cairo gtk3 libcanberra-gtk3
```

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, `cairo`, and `gobject-introspection` (and please let us know so we can improve this documentation!)

In addition to the dependencies above, if you would like to help add additional support for GTK4, you need to also install `gir1.2-gtk-4.0` on Ubuntu/Debian, or `gtk4` on Fedora or Arch. For other distributions, consult your distribution's platform documentation.

///

/// tab | Qt

These instructions are different on almost every version of Linux and Unix; here are some of the common alternatives:

### Ubuntu 24.10+ / Debian 13+

For Ubuntu 24.10+, the nessacary PySide6 modules should be installed through the system package manager in addition to the dependencies
above, and then the ``system-pyside6`` hack should be used in venv:

```console
(venv) $ sudo apt install python3-pyside6.qtcore python3-pyside6.qtwidgets python3-pyside6.qtgui python3-pyside6.qtquickwidgets
```

### Ubuntu 22.04 to 24.04 / Debian 11, 12

PySide6 (Python bindings for Qt) cannot be installed through the system; therefore installing it in venv (described
later) is required.

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git python3-dev qt6-base-dev libxcb-cursor0 gnome-session-canberra
```

### Fedora 41+

/// warning | Requirement to Update System Packages

Fedora's packaging of some Qt and KDE-related packages lists incorrect dependencies; installing PySide6 components
will force some of those packages to upgrade incorrectly and lead to missing symbols upon boot.  Therefore it is
extremely important to **upgrade all packages** after installing PySide6.  If you do not want this risk to be taken,
install PySide6 in the venv instead of using system packages.

///

```console
(venv) $ sudo dnf install git python3-devel python3-pyside6 libcanberra-gtk3
(venv) $ sudo dnf upgrade --refresh
```

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, PySide6, and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)

///

Some widgets (most notably, the [WebView][webview-system-requires] and [MapView][mapview-system-requires] widgets) have additional system requirements. Likewise, certain hardware features ([Location][location-system-requires]) have system requirements.

See the documentation of those widgets and hardware features for details.
