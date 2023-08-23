Label
=====

A text label for annotating forms or interfaces.

.. figure:: /reference/images/Label.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(Label|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    label = toga.Label("Hello world")

Notes
-----

* Winforms does not support an alignment value of ``JUSTIFIED``. If this
  alignment value is used, the label will default to left alignment.

Reference
---------

.. autoclass:: toga.Label
