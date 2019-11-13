Number Input
============

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(NumberInput|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16

The Number input is a text input box that is limited to numeric input.

.. figure:: /reference/images/NumberInput.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    textbox = toga.NumberInput(min_value=1, max_value=10)

Reference
---------

.. autoclass:: toga.widgets.numberinput.NumberInput
   :members:
   :undoc-members:
   :inherited-members:
