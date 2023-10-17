MainWindow
==========

The main window of the application.

.. figure:: /reference/images/MainWindow.png
   :align: center
   :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(MainWindow|Component))'}

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
