Text Input
==========

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|   |y|       |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The text input widget is a simple input field for user entry of text data.

.. figure:: /reference/images/TextInput.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    input = toga.TextInput(placeholder='enter name here')

Reference
---------

.. autoclass:: toga.widgets.textinput.TextInput
   :members:
   :undoc-members:
   :inherited-members:
