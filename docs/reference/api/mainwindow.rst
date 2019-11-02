MainWindow
==========

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(MainWindow|Component))'}

.. |y| image:: /_static/yes.png
    :width: 16

A window for displaying components to the user

Usage
-----

A MainWindow is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: Python

    import toga

    window = toga.MainWindow('id-window', title='This is a window!')
    window.show()

Reference
---------

.. autoclass:: toga.app.MainWindow
   :members:
   :undoc-members:
   :inherited-members:
