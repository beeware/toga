MainWindow
==========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(MainWindow|Component))'}

A window for displaying components to the user

Usage
-----

A MainWindow is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: python

    import toga

    window = toga.MainWindow('id-window', title='This is a window!')
    window.show()

Reference
---------

.. autoclass:: toga.MainWindow
   :members:
   :undoc-members:
