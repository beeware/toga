These instructions are different on almost every version of Linux and Unix; here are
some of the common alternatives:

..
    The package list should be the same as in ci.yml, and the BeeWare tutorial
    (CI will also have WebView requirements)

**Ubuntu / Debian**

.. code-block:: console

    (venv) $ sudo apt update
    (venv) $ sudo apt install git build-essential pkg-config python3-dev libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0 libcanberra-gtk3-module

**Fedora**

.. code-block:: console

    (venv) $ sudo dnf install git gcc make pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel gtk3 libcanberra-gtk3

**Arch / Manjaro**

.. code-block:: console

    (venv) $ sudo pacman -Syu git base-devel pkgconf python3 gobject-introspection cairo gtk3 libcanberra

**OpenSUSE Tumbleweed**

.. code-block:: console

    (venv) $ sudo zypper install git patterns-devel-base-devel_basis pkgconf-pkg-config python3-devel gobject-introspection-devel cairo-devel gtk3 'typelib(Gtk)=3.0' libcanberra-gtk3-module

**FreeBSD**

.. code-block:: console

    (venv) $ sudo pkg update
    (venv) $ sudo pkg install git gcc cmake pkgconf python3 gobject-introspection cairo gtk3 libcanberra-gtk3

If you're not using one of these, you'll need to work out how to install the developer
libraries for ``python3``, ``cairo``, and ``gobject-introspection`` (and please let us
know so we can improve this documentation!)

In addition to the dependencies above, if you would like to help add additional support
for GTK4, you need to also install ``gir1.2-gtk-4.0`` or equivalent on your system.

Some widgets (most notably, the :ref:`WebView <webview-system-requires>` and
:ref:`MapView <mapview-system-requires>` widgets) have additional system requirements.
Likewise, certain hardware features (:ref:`Location <location-system-requires>`) have
system requirements.

See the documentation of those widgets and hardware features for details.
