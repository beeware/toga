Option Container
================

The Option Container widget is a user-selection control for choosing from a pre-configured list of controls, like a tab view.

Usage
-----

.. code-block:: Python

    import toga
    
    container = toga.OptionContainer()

    table = toga.Table(['Hello', 'World'])
    tree = toga.Tree(['Navigate'])

    container.add('Table', table)
    container.add('Tree', tree)

Supported Platforms
-------------------

.. include:: ../supported_platforms/OptionContainer.rst

Reference
---------

.. autoclass:: toga.interface.widgets.optioncontainer.OptionContainer
   :members:
   :undoc-members:
   :inherited-members:
