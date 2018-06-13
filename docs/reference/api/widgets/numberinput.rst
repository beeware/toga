Number Input
============

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|      |y|     |y|
======= ====== ========= ===== ========= ========

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
