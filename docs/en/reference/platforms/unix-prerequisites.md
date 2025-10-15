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
above, and then the ``system-pyside6`` hack should be used in venv.  Installing PySide6 automatically installs Qt itself.

```console
(venv) $ sudo apt install git python3-dev build-essential \
             python3-pyside6.qtcore python3-pyside6.qtwidgets \
             python3-pyside6.qtgui python3-pyside6.qtquickwidgets \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             libwayland-dev libwayland-egl1-mesa libwayland-server0 \
             libgles2-mesa-dev libxkbcommon-dev
```

### Ubuntu 22.04 to 24.04 / Debian 11, 12

PySide6 (Python bindings for Qt) cannot be installed through the system; therefore installing it in venv (described
later) is required.  This means that we can just install the dependencies for Qt here, as Qt itself will be provided
by PySide6 in ``pip`` with the caveat that it does not integrate with system themes:

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git python3-dev build-essential \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             libwayland-dev libwayland-egl1-mesa libwayland-server0 \
             libgles2-mesa-dev libxkbcommon-dev
```

### Fedora 41+

/// warning | Requirement to Update System Packages

Fedora's packaging of some Qt and KDE-related packages lists incorrect dependencies; installing PySide6 components
will force some of those packages to upgrade incorrectly and lead to missing symbols upon boot.  Therefore it is
extremely important to **upgrade all packages** after installing PySide6.  If you do not want this risk to be taken,
install PySide6 in the venv only (remove ``python3-pyside6`` from the list below), and use that instead of ``system-pyside6``.

///

```console
(venv) $ sudo dnf install git python3-devel python3-pyside6 \
             libcanberra-gtk3 fontconfig-devel freetype-devel \
             gtk3-devel libX11-devel libX11-xcb libXext-devel \
             libXfixes-devel libXi-devel libxkbcommon-devel \
             libxkbcommon-x11-devel libXrender-devel 'xcb-util*devel' \
             wayland-devel libwayland-server mesa-libEGL
(venv) $ sudo dnf upgrade --refresh
```

Again, a ``system-pyside6`` package must be installed in the venv.

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, [Qt's X11 dependencies](https://doc.qt.io/qt-6/linux-requirements.html), [Qt's Wayland dependencies](https://doc.qt.io/qt-6/wayland-requirements.html), and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)

///

Some widgets (most notably, the [WebView][webview-system-requires] and [MapView][mapview-system-requires] widgets) have additional system requirements. Likewise, certain hardware features ([Location][location-system-requires]) have system requirements.

See the documentation of those widgets and hardware features for details.
