Label
=====

A text label for annotating forms or interfaces.

.. figure:: /reference/images/Label.jpeg
    :align: center

Availability
------------
.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Label|Component)$)'}

Usage
-----

.. code-block:: Python

    import toga

    label = toga.Label('Hello world')

Reference
---------

.. autoclass:: toga.widgets.label.Label
   :members:
