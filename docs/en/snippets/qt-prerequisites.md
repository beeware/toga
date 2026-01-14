<!-- rumdl-disable-line MD041 -->

These instructions are different on almost every version of Linux and Unix, in addition to whether Wayland or X11 is used; here are some of the common alternatives:

### Ubuntu 24.04 / Debian 11+

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

You can use [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) (or a similar third-party source) to install a Python version other than the system default by replacing `python3-dev` with the `-dev` package matching the desired Python version. For example, to use Python 3.12, replace `python3-dev` with `python3.12-dev`.

### Fedora 41+

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

You can use a Python version other than the system default by replacing `python3-devel` with the `-devel` package matching the desired Python version. For example, to use Python 3.12, replace `python3-devel` with `python3.12-devel`.

### Other distributions

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, [Qt's X11 dependencies](https://doc.qt.io/qt-6/linux-requirements.html), [Qt's Wayland dependencies](https://doc.qt.io/qt-6/wayland-requirements.html), and the executable ``canberra-gtk-play`` (and please let us know so we can improve this documentation!)
