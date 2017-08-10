:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Selection
=========

The Selection widget is a simple control for allowing the user to choose between a list of string options.

.. figure:: /reference/images/Selection.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga
        
    container = toga.Selection(items=['bob', 'jim', 'lilly'])

Supported Platforms
-------------------

.. include:: ../supported_platforms/Selection.rst

Reference
---------

.. autoclass:: toga.widgets.selection.Selection
   :members:
   :undoc-members:
   :inherited-members: