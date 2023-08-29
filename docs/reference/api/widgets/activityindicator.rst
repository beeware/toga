ActivityIndicator
=================

A small animated indicator showing activity on a task of indeterminate length,
usually rendered as a "spinner" animation.

.. figure:: /reference/images/ActivityIndicator.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(ActivityIndicator|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    indicator = toga.ActivityIndicator()

    # Start the animation
    indicator.start()

    # Stop the animation
    indicator.stop()

Notes
-----

* The ActivityIndicator will always take up a fixed amount of physical space in
  a layout. However, the widget will not be visible when it is in a "stopped"
  state.

Reference
---------

.. autoclass:: toga.ActivityIndicator
