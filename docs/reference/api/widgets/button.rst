Button
======

A button that can be pressed or clicked.

.. figure:: /reference/images/Button.jpeg
    :align: center
    :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Button|Component))'}

Usage
-----

A button has a text label. A handler can be associated with button press events.

.. code-block:: python

    import toga

    def my_callback(button):
        # handle event
        pass

    button = toga.Button("Click me", on_press=my_callback)

Notes
-----

* A background color of ``TRANSPARENT`` will be treated as a reset of the button
  to the default system color.

* On macOS, the button text color cannot be set directly; any ``color`` style
  directive will be ignored. The text color is automatically selected by
  the platform to contrast with the background color of the button.

Reference
---------

.. autoclass:: toga.Button

.. autoprotocol:: toga.widgets.button.OnPressHandler
