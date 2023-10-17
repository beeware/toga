Window
======

An operating system-managed container of widgets.

.. figure:: /reference/images/Window.png
   :align: center
   :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Window|Component))'}

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

The operating system may provide controls that allow the user to resize, reposition,
minimize, maximize or close the window. However, the availability of these controls is
entirely operating system dependent.

If the user attempts to close the window, Toga will call the ``on_close`` handler. This
handler must return a ``bool`` confirming whether the close is permitted. This can be
used to implement protections against closing a window with unsaved changes.

Once a window has been closed (either by user action, or programmatically with
:meth:`~toga.Window.close()`), it *cannot* be reused. The behavior of any method on a
:class:`~toga.Window` instance after it has been closed is undefined.

Notes
-----

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
