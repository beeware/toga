OptionContainer
===============

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(OptionContainer|Component))'}

The Option Container widget is a user-selection control for choosing from a pre-configured list of controls, like a tab view.

.. figure:: /reference/images/OptionContainer.jpeg
    :align: center

Usage
-----

.. code-block:: python

    import toga

    container = toga.OptionContainer()

    table = toga.Table(['Hello', 'World'])
    tree = toga.Tree(['Navigate'])

    container.add('Table', table)
    container.add('Tree', tree)

Reference
---------

.. autoclass:: toga.OptionContainer
   :members:
   :undoc-members:
