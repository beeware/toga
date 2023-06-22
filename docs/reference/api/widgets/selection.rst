Selection
=========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Selection|Component)$)'}

The Selection widget is a simple control for allowing the user to choose between a list of string options.

.. figure:: /reference/images/Selection.jpeg
    :align: center

Usage
-----

.. code-block:: python

    import toga

    container = toga.Selection(items=['bob', 'jim', 'lilly'])

Reference
---------

.. autoclass:: toga.Selection
   :members:
   :undoc-members:
