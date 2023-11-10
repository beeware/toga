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

As the main window is closely bound to the App, a main window *cannot* define an
``on_close`` handler. Instead, if you want to prevent the main window from exiting, you
should use an ``on_exit`` handler on the :class:`toga.App` that the main window is
associated with.

Reference
---------

.. autoclass:: toga.MainWindow
