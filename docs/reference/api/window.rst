Window
======

An operating system-managed container of widgets.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/window-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/window-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/window-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android |no|

    Not supported

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

A window is the top-level container that the operating system uses to display widgets. A
window may also have other decorations, such as a title bar or toolbar.

When first created, a window is not visible. To display it, call the
:meth:`~toga.Window.show` method.

The window has content, which will usually be a container widget of some kind. The
content of the window can be changed by re-assigning its `content` attribute to a
different widget.

.. code-block:: python

    import toga

    window = toga.Window()
    window.content = toga.Box(children=[...])
    window.show()

    # Change the window's content to something new
    window.content = toga.Box(children=[...])

If the user attempts to close the window, Toga will call the ``on_close`` handler. This
handler must return a ``bool`` confirming whether the close is permitted. This can be
used to implement protections against closing a window with unsaved changes.

Once a window has been closed (either by user action, or programmatically with
:meth:`~toga.Window.close()`), it *cannot* be reused. The behavior of any method on a
:class:`~toga.Window` instance after it has been closed is undefined.

Notes
-----
* The operating system may provide controls that allow the user to resize, reposition,
  minimize, maximize or close the window. However, the availability of these controls
  is entirely operating system dependent.

* While Toga provides methods for specifying the size and position of windows,
  these are ultimately at the discretion of the OS (or window manager). For
  example, on macOS, depending on a user's OS-level settings, new windows may
  open as tabs on the main window; on Linux, some window managers (e.g., tiling
  window managers) may not honor an app's size and position requests. You should
  avoid making UI design decisions that are dependent on specific size and
  placement of windows.

* A mobile application can only have a single window (the :class:`~toga.MainWindow`),
  and that window cannot be moved, resized, hidden, or made full screen. Toga will raise
  an exception if you attempt to create a secondary window on a mobile platform. If you
  try to modify the size, position, or visibility of the main window, the request will
  be ignored.

Reference
---------

.. autoclass:: toga.Window

.. autoprotocol:: toga.window.OnCloseHandler
.. autoprotocol:: toga.window.DialogResultHandler
