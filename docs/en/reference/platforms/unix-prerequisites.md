<!-- rumdl-disable-line MD041 -->

These instructions are different on almost every version of Linux and Unix; here are some of the common alternatives:

# Ubuntu 24.04+ / Debian 13+

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git build-essential pkg-config python3-dev libgirepository-2.0-dev libcairo2-dev gir1.2-gtk-3.0 libcanberra-gtk3-module
```

## Ubuntu 22.04 / Debian 11, 12

```console
(venv) $ sudo apt update
(venv) $ sudo apt install git build-essential pkg-config python3-dev libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0 libcanberra-gtk3-module
```

If you're running on Ubuntu 22.04, Debian 11 or Debian 12, you'll also need to add a pin for `PyGObject==3.50.0`. Later versions of PyGObject require the `libgirepository-2.0-dev` library, which isn't available on older Debian-based distributions.

## Fedora

```console
(venv) $ sudo dnf install git gcc make pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel gtk3 libcanberra-gtk3
```

## Arch / Manjaro

```console
(venv) $ sudo pacman -Syu git base-devel pkgconf python3 gobject-introspection cairo gtk3 libcanberra
```

## OpenSUSE Tumbleweed

```console
(venv) $ sudo zypper install git patterns-devel-base-devel_basis pkgconf-pkg-config python3-devel gobject-introspection-devel cairo-devel gtk3 'typelib(Gtk)=3.0' libcanberra-gtk3-module
```

## FreeBSD

```console
(venv) $ sudo pkg update
(venv) $ sudo pkg install git gcc cmake pkgconf python3 gobject-introspection cairo gtk3 libcanberra-gtk3
```

If you're not using one of these, you'll need to work out how to install the developer libraries for `python3`, `cairo`, and `gobject-introspection` (and please let us know so we can improve this documentation!)

In addition to the dependencies above, if you would like to help add additional support for GTK4, you need to also install `gir1.2-gtk-4.0` on Ubuntu/Debian, or `gtk4` on Fedora or Arch. For other distributions, consult your distribution's platform documentation.

Some widgets (most notably, the [WebView][webview-system-requires] and [MapView][mapview-system-requires] widgets) have additional system requirements. Likewise, certain hardware features ([Location][location-system-requires]) have system requirements.

See the documentation of those widgets and hardware features for details.
