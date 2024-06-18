MainWindow
==========

The main window of the application.

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

The main window of an application is a normal :class:`toga.Window`, with one exception -
when the main window is closed, the application exits.

.. code-block:: python

    import toga

    main_window = toga.MainWindow(title='My Application')

    self.toga.App.main_window = main_window
    main_window.show()

Reference
---------

.. autoclass:: toga.MainWindow
