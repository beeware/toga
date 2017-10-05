:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Split Container
===============

The split container is a container with a movable split and the option for 2 or 3 elements.

.. figure:: /reference/images/SplitContainer.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    split = toga.SplitContainer()
    left_container = toga.Box()
    right_container = toga.ScrollContainer()
    
    split.content = [left_container, right_container]
    
Setting split direction
-----------------------

Split direction is set on instantiation using the `direction` keyword argument. Direction is vertical by default.

.. code-block:: Python

    import toga

    split = toga.SplitContainer()
    left_container = toga.Box()
    right_container = toga.ScrollContainer(direction=toga.ScrollContainer.HORIZONTAL)
    
    split.content = [left_container, right_container]

Supported Platforms
-------------------

.. include:: ../supported_platforms/SplitContainer.rst

Reference
---------

.. autoclass:: toga.widgets.splitcontainer.SplitContainer
   :members:
   :undoc-members:
   :inherited-members: