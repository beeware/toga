==========
Linux/Unix
==========

.. image:: /reference/screenshots/gtk.png
   :align: center
   :width: 300

The Toga backend for Linux (and other Unix-like operating systems) is `toga-gtk
<https://github.com/beeware/toga/tree/main/gtk>`__.

.. admonition:: Qt support

    Toga does not currently have a Qt backend for KDE-based desktops. However, we would
    like to add one; see `this ticket <https://github.com/beeware/toga/issues/1142>`__
    for details. If you would like to contribute, please get in touch on that ticket, on
    `Mastodon <https://fosstodon.org/@beeware>`__ or on `Discord
    <https://beeware.org/bee/chat/>`__.

.. admonition:: GTK on Windows and macOS

    Although GTK *can* be installed on Windows and macOS, and the ``toga-gtk`` backend
    *may* work on those platforms, this is not officially supported by Toga. We
    recommend using ``toga-winforms`` on Windows, and ``toga-cocoa`` on macOS.

Prerequisites
-------------

``toga-gtk`` requires GTK 3.22 or newer. This requirement can be met with with all
versions of Ubuntu since 18.04, and all versions of Fedora since Fedora 26.

Toga receives the most testing with GTK 3.24. This is the version that has shipped with
all versions of Ubuntu since Ubuntu 20.04, and all versions of Fedora since Fedora 29.

The system packages that provide GTK must be installed manually:

.. include:: /reference/platforms/unix-prerequisites.rst

Toga does not currently support GTK 4.

Installation
------------

``toga-gtk`` is installed automatically on any Linux machine (machines that report
``sys.platform == 'linux'``), or any FreeBSD machine (machines that report
``sys.platform == 'freebsd*'``). It can be manually installed by running:

.. code-block:: console

    $ python -m pip install toga-gtk

Implementation details
----------------------

``toga-gtk`` uses the native GObject Python bindings.
