NumberInput
===========

A text input that is limited to numeric input.

.. figure:: /reference/images/NumberInput.png
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(NumberInput|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    widget = toga.NumberInput(min_value=1, max_value=10, step=0.001)
    widget.value = 2.718

NumberInput's properties can accept integers, floats, and strings containing
numbers, but they always return :any:`decimal.Decimal` objects to ensure
precision is retained.

Reference
---------

.. autoclass:: toga.NumberInput
