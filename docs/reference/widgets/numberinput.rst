:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Number Input
============

The Number input is a text input box that is limited to numeric input.

.. figure:: /reference/images/NumberInput.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga
    
    textbox = toga.NumberInput(min_value=1, max_value=10)

Supported Platforms
-------------------

.. include:: ../supported_platforms/NumberInput.rst

Reference
---------

.. autoclass:: toga.widgets.numberinput.NumberInput
   :members:
   :undoc-members:
   :inherited-members: