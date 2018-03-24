Button
======

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|   |y|       |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The button is a clickable node that fires a callback method when pressed or clicked.

.. figure:: /reference/images/Button.jpeg
    :align: center
    :width: 300

Usage
-----

The most basic button has a text label and a callback method for when it is pressed. The callback expects 1 argument, the instance of the button firing the event.

.. code-block:: Python

    import toga

    def my_callback(button):
        # handle event
        pass

    button = toga.Button('Click me', on_press=my_callback)

Reference
---------

.. autoclass:: toga.widgets.button.Button
   :members:
   :undoc-members:
   :inherited-members:
