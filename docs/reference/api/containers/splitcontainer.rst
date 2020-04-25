Split Container
===============

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(SplitContainer|Component))'}

.. |y| image:: /_static/yes.png
    :width: 16

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

    split = toga.SplitContainer(direction=toga.SplitContainer.HORIZONTAL)
    left_container = toga.Box()
    right_container = toga.ScrollContainer()

    split.content = [left_container, right_container]

Reference
---------

.. autoclass:: toga.widgets.splitcontainer.SplitContainer
   :members:
   :undoc-members:
   :inherited-members:
