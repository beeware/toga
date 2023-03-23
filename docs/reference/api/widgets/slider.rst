Slider
======

A widget for selecting a value within a range, displayed as a horizontal line.

.. figure:: /reference/images/Slider.png
    :align: center
    :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Slider|Component)$)'}


Usage
-----

.. code-block:: Python

    import toga

    def my_callback(slider):
        print(slider.value)

    slider = toga.Slider(value=5, range=(-10, 10), on_change=my_callback)


Reference
---------

.. autoclass:: toga.widgets.slider.Slider
   :members:
   :undoc-members:
