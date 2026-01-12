<!-- rumdl-disable-line MD041 -->

These instructions are different on almost every version of Linux and Unix, in addition to whether Wayland or X11 is used; here are some of the common alternatives:

### Ubuntu 24.04 / Debian 11+

For specific python version (e.g., 3.12) replace `python3-dev` to `python3.12-dev`.

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

### Fedora 41+

/// warning | Requirement to Update System Packages

Fedora's packaging of some Qt and KDE-related packages lists incorrect dependency versions; installing certain packages that updates KWin or related things may brick your system.  Therefore, it is highly recommended, as a general precaution, to upgrade all packages following the installation of these components.

///

For specific python version (e.g., 3.12) replace `python3-devel` to `python3.12-devel`.

/// tab | Wayland

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 wayland-devel libwayland-server \
             mesa-libEGL libxkbcommon-devel
(venv) $ sudo dnf upgrade --refresh
```

///

/// tab | X11

```console
(venv) $ sudo dnf install git python3-devel \
             libcanberra-gtk3 fontconfig-devel freetype-devel \
             gtk3-devel libX11-devel libX11-xcb libXext-devel \
             libXfixes-devel libXi-devel libxkbcommon-devel \
             libxkbcommon-x11-devel libXrender-devel 'xcb-util*devel' \
(venv) $ sudo dnf upgrade --refresh
```

///

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, [Qt's X11 dependencies](https://doc.qt.io/qt-6/linux-requirements.html), [Qt's Wayland dependencies](https://doc.qt.io/qt-6/wayland-requirements.html), and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)
