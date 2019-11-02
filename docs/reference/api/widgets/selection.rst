Selection
=========

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Selection|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16

The Selection widget is a simple control for allowing the user to choose between a list of string options.

.. figure:: /reference/images/Selection.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    container = toga.Selection(items=['bob', 'jim', 'lilly'])

Reference
---------

.. autoclass:: toga.widgets.selection.Selection
   :members:
   :undoc-members:
   :inherited-members:
