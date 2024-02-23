MainWindow
==========

A window that can be used as the main interface to an app.

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

A main window of an application is a :class:`toga.Window` that can serve as the main
interface to an application. If the platform places menus inside windows, a
:class:`toga.MainWindow` instance  will display a menu bar that contains the app control
commands (such as About, Quit, and anything else required by the platform's HIG). It may
also contain a toolbar.

The title of the window will default to the formal name of the app.

.. code-block:: python

    import toga

    main_window = toga.MainWindow()

    self.toga.App.main_window = main_window
    main_window.show()

Reference
---------

.. autoclass:: toga.MainWindow
