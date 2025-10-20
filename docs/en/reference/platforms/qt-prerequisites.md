<!-- rumdl-disable-line MD041 -->

These instructions are different on almost every version of Linux and Unix, in addition to whether Wayland or X11 is used; here are some
of the common alternatives:

#### Ubuntu 24.10+ / Debian 13+

For Ubuntu 24.10+, the necessary PySide6 modules should be installed through the system package manager in addition to the dependencies
above, and then the ``system`` extra of ``toga_qt`` should be installed in the virtual environment.  Installing PySide6 automatically
installs Qt itself.

/// tab | Wayland

```console
(venv) $ sudo apt install git python3-dev build-essential \
             python3-pyside6.qtcore python3-pyside6.qtwidgets \
             python3-pyside6.qtgui python3-pyside6.qtquickwidgets \
             libwayland-dev libwayland-egl1-mesa libwayland-server0 \
             libgles2-mesa-dev libxkbcommon-dev gnome-session-canberra
```

///

/// tab | X11

```console
(venv) $ sudo apt install git python3-dev build-essential \
             python3-pyside6.qtcore python3-pyside6.qtwidgets \
             python3-pyside6.qtgui python3-pyside6.qtquickwidgets \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             gnome-session-canberra
```

///

#### Ubuntu 22.04 to 24.04 / Debian 11, 12

PySide6 (Python bindings for Qt) cannot be installed through the system; therefore installing it in your virtual environment (described
later) is required.  This means that we can just install the dependencies for Qt here, as Qt itself will be provided
by PySide6 in ``pip`` with the caveat that it does not integrate with system themes.  The ``pyside6`` extra of ``toga_qt`` should be used.

/// tab | Wayland

```console
(venv) $ sudo apt install git python3-dev build-essential \
             libwayland-dev libwayland-egl1-mesa libwayland-server0 \
             libgles2-mesa-dev libxkbcommon-dev gnome-session-canberra
```

///

/// tab | X11

```console
(venv) $ sudo apt install git python3-dev build-essential \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             gnome-session-canberra
```

///

#### Fedora 41+

/// warning | Requirement to Update System Packages

Fedora's packaging of some Qt and KDE-related packages lists incorrect dependency versions; installing PySide6 components
will force some of those packages to upgrade incorrectly and lead to missing symbols upon boot.  Therefore it is
extremely important to **upgrade all packages** after installing PySide6.  If you do not want this risk to be taken,
install PySide6 in a virtual environment only (remove ``python3-pyside6`` from the list below), and use the ``pyside6``
extra instead of ``system`` extra when installing ``toga_qt``.

///

/// tab | Wayland

```console
(venv) $ sudo dnf install git python3-devel python3-pyside6 \
             libcanberra-gtk3 wayland-devel libwayland-server \
             mesa-libEGL libxkbcommon-devel
(venv) $ sudo dnf upgrade --refresh
```

///

/// tab | X11

```console
(venv) $ sudo dnf install git python3-devel python3-pyside6 \
             libcanberra-gtk3 fontconfig-devel freetype-devel \
             gtk3-devel libX11-devel libX11-xcb libXext-devel \
             libXfixes-devel libXi-devel libxkbcommon-devel \
             libxkbcommon-x11-devel libXrender-devel 'xcb-util*devel' \
(venv) $ sudo dnf upgrade --refresh
```

///

Again, the ``system`` extra of ``toga_qt`` shall be used.

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, [Qt's X11 dependencies](https://doc.qt.io/qt-6/linux-requirements.html), [Qt's Wayland dependencies](https://doc.qt.io/qt-6/wayland-requirements.html), and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)
