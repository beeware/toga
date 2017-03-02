Split Container
===============

The split container is a container with a movable split and the option for 2 or 3 elements. 

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

.. autoclass:: toga.interface.widgets.splitcontainer.SplitContainer
   :members:
   :undoc-members:
   :inherited-members: