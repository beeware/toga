<!-- rumdl-disable-line MD041 -->

`toga-qt` depends on the PySide6 Qt bindings. However, there are 2 ways to access these bindings: using the bindings provided by your operating system; or by installing the bindings that are published on PyPI.

If you install the PySide6 bindings from PyPI, your application will *not* integrate with any themes provided by your operating system. If you are using a Qt-based desktop environment (such as KDE), this will result in an application that doesn't match the appearance of the rest of your system. An app using the system-provided bindings will also be significantly smaller than one using standalone bindings, as the standalone bindings contain a complete copy of Qt.

The process of installing pre-requisites is different on almost every version of Linux and Unix, and is affected by the use of Wayland or X11, and whether the system PySide6 bindings are used. Here are some of the common alternatives:

### Ubuntu 24.10+ / Debian 13+

/// tab | Wayland (System)

```console
(venv) $ sudo apt install git python3-dev build-essential \
             python3-pyside6.qtcore python3-pyside6.qtwidgets \
             python3-pyside6.qtgui python3-pyside6.qtquickwidgets \
             python3-pyside6.qtpositioning python3-pyside6.qtwebenginecore \
             python3-pyside6.qtwebenginewidgets \
             libwayland-dev libwayland-server0 libwayland-egl1 \
             libgles2-mesa-dev libxkbcommon-dev gnome-session-canberra \
             qt6-wayland
```

///

/// tab | X11 (System)

```console
(venv) $ sudo apt install git python3-dev build-essential \
             python3-pyside6.qtcore python3-pyside6.qtwidgets \
             python3-pyside6.qtgui python3-pyside6.qtquickwidgets \
             python3-pyside6.qtpositioning python3-pyside6.qtwebenginecore \
             python3-pyside6.qtwebenginewidgets \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             gnome-session-canberra
```

///

/// tab | Wayland (Standalone)

```console
(venv) $ sudo apt install git python3-dev build-essential \
             libwayland-dev libwayland-server0 libwayland-egl1 \
             libgles2-mesa-dev libxkbcommon-dev gnome-session-canberra
```

///

/// tab | X11 (Standalone)

```console
(venv) $ sudo apt install git python3-dev build-essential \
             libfontconfig1-dev libfreetype-dev libgtk-3-dev \
             libx11-dev libx11-xcb-dev libxext-dev \
             libxfixes-dev libxi-dev libxkbcommon-dev \
             libxkbcommon-x11-dev libxrender-dev 'libxcb*-dev' \
             gnome-session-canberra
```

///

You can use [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) (or a similar third-party source) to install a Python version other than the system default by replacing `python3-dev` with the `-dev` package matching the desired Python version. For example, to use Python 3.12, replace `python3-dev` with `python3.12-dev`.

### Fedora 41+

/// tab | Wayland (System)

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 wayland-devel libwayland-server \
             mesa-libEGL libxkbcommon-devel python3-pyside6 \
             qt6-qtwayland
(venv) $ sudo dnf upgrade --refresh
```

///

/// tab | X11 (System)

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 fontconfig-devel freetype-devel \
             gtk3-devel libX11-devel libX11-xcb libXext-devel \
             libXfixes-devel libXi-devel libxkbcommon-devel \
             libxkbcommon-x11-devel libXrender-devel 'xcb-util*devel' \
             python3-pyside6
(venv) $ sudo dnf upgrade --refresh
```

///

/// tab | Wayland (Standalone)

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 wayland-devel libwayland-server \
             mesa-libEGL libxkbcommon-devel
(venv) $ sudo dnf upgrade --refresh
```

///

/// tab | X11 (Standalone)

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 fontconfig-devel freetype-devel \
             gtk3-devel libX11-devel libX11-xcb libXext-devel \
             libXfixes-devel libXi-devel libxkbcommon-devel \
             libxkbcommon-x11-devel libXrender-devel 'xcb-util*devel'
(venv) $ sudo dnf upgrade --refresh
```

///

You can use a Python version other than the system default by replacing `python3-devel` with the `-devel` package matching the desired Python version. For example, to use Python 3.12, replace `python3-devel` with `python3.12-devel`.

### Other distributions

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, PySide6, Qt 6, [Qt's X11 dependencies](https://doc.qt.io/qt-6/linux-requirements.html), [Qt's Wayland dependencies](https://doc.qt.io/qt-6/wayland-requirements.html), and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)
