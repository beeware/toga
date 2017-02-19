Split Container
===============

The split container

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

Reference
---------

.. autoclass:: toga.interface.widgets.splitcontainer.SplitContainer
   :members:
   :undoc-members:
   :inherited-members: