ComboBox
========

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
         |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The ComboBox widget is a free entry input field that provides options to the user.

Usage
-----

.. code-block:: Python

    import toga

    container = toga.ComboBox(initial='toga', items=['batavia', 'voc', 'beekeeper'])

Reference
---------

.. autoclass:: toga.widgets.combobox.ComboBox
   :members:
   :undoc-members:
   :inherited-members:
