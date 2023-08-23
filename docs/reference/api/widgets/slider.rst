Slider
======

A widget for selecting a value within a range. The range is shown as a horizontal line,
and the selected value is shown as a draggable marker.

.. figure:: /reference/images/Slider.png
    :align: center
    :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(Slider|Component)$)'}


Usage
-----

A slider can either be continuous (allowing any value within the range), or discrete
(allowing a fixed number of equally-spaced values). For example:

.. code-block:: python

    import toga

    def my_callback(slider):
        print(slider.value)

    # Continuous slider, with an event handler.
    toga.Slider(range=(-5, 10), value=7, on_change=my_callback)

    # Discrete slider, accepting the values [0, 1.5, 3, 4.5, 6, 7.5].
    toga.Slider(range=(0, 7.5), tick_count=6)


Reference
---------

.. autoclass:: toga.Slider
