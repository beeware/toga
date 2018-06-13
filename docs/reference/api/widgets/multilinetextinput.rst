Multi-line text input
=====================

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The Multi-line text input is similar to the text input but designed for larger inputs, similar to the textarea field of HTML.

Usage
-----

.. code-block:: Python

    import toga

    textbox = toga.MultilineTextInput(id='view1')

Reference
---------

.. autoclass:: toga.widgets.multilinetextinput.MultilineTextInput
   :members:
   :undoc-members:
   :inherited-members:
