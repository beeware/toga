These instructions are different on almost every version of Linux and Unix; here are
some of the common alternatives:

..
    The package list should be the same as in ci.yml, and the BeeWare tutorial
    (CI will also have WebView requirements)

**Ubuntu 18.04+ / Debian 11+**

.. code-block:: console

    (venv) $ sudo apt update
    (venv) $ sudo apt install pkg-config python3-dev libgirepository1.0-dev libcairo2-dev libcanberra-gtk3-module

**Fedora**

.. code-block:: console

    (venv) $ sudo dnf install pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel libcanberra-gtk3

**Arch / Manjaro**

.. code-block:: console

    (venv) $ sudo pacman -Syu git pkgconf gobject-introspection cairo libcanberra

**FreeBSD**

.. code-block:: console

    (venv) $ sudo pkg update
    (venv) $ sudo pkg install gobject-introspection cairo libcanberra-gtk3

If you're not using one of these, you'll need to work out how to install the developer
libraries for ``python3``, ``cairo``, and ``gobject-introspection`` (and please let us
know so we can improve this documentation!)

Some widgets (most notably, the :ref:`WebView <webview-system-requires>` and
:ref:`MapView <mapview-system-requires>` widgets) have additional system requirements.
See the documentation of those widgets for details.
