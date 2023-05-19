NumberInput
===========

A text input that is limited to numeric input.

.. figure:: /reference/images/NumberInput.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(NumberInput|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    widget = toga.NumberInput(min_value=1, max_value=10)
    widget.value = 2.71828

Although NumberInput can accept integers and floats as inputs, the value
returned by a NumberInput will be a ``decimal.Decimal`` object to ensure
precision is retained.

Reference
---------

.. autoclass:: toga.widgets.numberinput.NumberInput
   :members:
   :undoc-members:
