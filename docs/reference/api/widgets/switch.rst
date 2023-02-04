Switch
======

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Switch|Component)$)'}

The switch widget is a clickable button with two stable states, True (on,
checked) and False (off, unchecked).

Usage
-----

.. code-block:: Python

    import toga

    input = toga.Switch()


Reference
---------

.. autoclass:: toga.widgets.switch.Switch
   :members:
   :undoc-members:
