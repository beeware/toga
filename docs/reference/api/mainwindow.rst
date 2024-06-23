MainWindow
==========

A window that can use the full set of window-level user interface elements.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/mainwindow-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/mainwindow-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/mainwindow-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android

    .. figure:: /reference/images/mainwindow-android.png
       :align: center
       :width: 450px

  .. group-tab:: iOS

    .. figure:: /reference/images/mainwindow-iOS.png
       :align: center
       :width: 450px

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/mainwindow-web.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

  .. group-tab:: Textual |beta|

    .. .. figure:: /reference/images/mainwindow-textual.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

Usage
-----

A :class:`toga.MainWindow` is a :class:`toga.Window` that can serve as the main
interface to an application. If the platform places menus inside windows, a
:class:`toga.MainWindow` instance will display a menu bar that contains the app
control commands (such as About, Quit, and anything else required by the
platform's HIG). It may also contain a toolbar.

In addition to the platform's default commands, user-defined commands can be
added to the :class:`toga.MainWindow`'s menu by adding them to
:attr:`~toga.App.commands`. Toolbar items can be added by adding them to
:attr:`~toga.MainWindow.toolbar`; any command added to the toolbar will be
automatically added to the App's commands as well.

.. code-block:: python

    import toga

    main_window = toga.MainWindow(title='My Application')

    self.toga.App.main_window = main_window
    main_window.show()

Reference
---------

.. autoclass:: toga.MainWindow
