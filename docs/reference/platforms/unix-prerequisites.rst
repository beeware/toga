These instructions are different on almost every version of Linux and Unix; here are
some of the common alternatives:

..
    The package list should be the same as in ci.yml, and the BeeWare tutorial
    (CI will also have WebView requirements)

**Ubuntu / Debian**

.. code-block:: console

    (venv) $ sudo apt update
    (venv) $ sudo apt install gcc git pkg-config python3-dev gir1.2-gtk-3.0 libgirepository1.0-dev libcairo2-dev libcanberra-gtk3-module

**Fedora**

.. code-block:: console

    (venv) $ sudo dnf install gcc git pkg-config python3-devel gtk3 gobject-introspection-devel cairo-gobject-devel libcanberra-gtk3

**Arch / Manjaro**

.. code-block:: console

    (venv) $ sudo pacman -Syu gcc git pkgconf python3 gtk3 gobject-introspection cairo libcanberra

**OpenSUSE Tumbleweed**

.. code-block:: console

    (venv) $ sudo zypper install gcc git pkgconf-pkg-config python3-devel gtk3 'typelib(Gtk)=3.0' gobject-introspection-devel cairo-devel libcanberra-gtk3-0

**FreeBSD**

.. code-block:: console

    (venv) $ sudo pkg update
    (venv) $ sudo pkg install gcc cmake git python3 pkgconf gtk3 gobject-introspection cairo libcanberra-gtk3

If you're not using one of these, you'll need to work out how to install the developer
libraries for ``python3``, ``cairo``, and ``gobject-introspection`` (and please let us
know so we can improve this documentation!)

Some widgets (most notably, the :ref:`WebView <webview-system-requires>` and
:ref:`MapView <mapview-system-requires>` widgets) have additional system requirements.
See the documentation of those widgets for details.
