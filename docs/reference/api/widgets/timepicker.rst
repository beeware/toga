TimePicker
==========

A widget to select a clock time.

.. .. figure:: /reference/images/TimePicker.jpeg
..     :align: center
..     :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(TimePicker|Component))'}

Usage
-----

.. code-block:: python

    import toga

    current_time = toga.TimePicker()

Reference
---------

.. autoclass:: toga.widgets.timepicker.TimePicker
   :members:
   :undoc-members:
