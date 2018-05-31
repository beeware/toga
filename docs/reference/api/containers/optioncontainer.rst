Option Container
================

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The Option Container widget is a user-selection control for choosing from a pre-configured list of controls, like a tab view.

.. figure:: /reference/images/OptionContainer.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    container = toga.OptionContainer()

    table = toga.Table(['Hello', 'World'])
    tree = toga.Tree(['Navigate'])

    container.add('Table', table)
    container.add('Tree', tree)

Reference
---------

.. autoclass:: toga.widgets.optioncontainer.OptionContainer
   :members:
   :undoc-members:
   :inherited-members:
