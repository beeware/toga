SplitContainer
==============

A container that divides an area into two panels with a movable border.

.. figure:: /reference/images/SplitContainer.png
   :align: center
   :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(SplitContainer|Component))'}


Usage
-----

.. code-block:: python

    import toga

    left_container = toga.Box()
    right_container = toga.ScrollContainer()

    split = toga.SplitContainer(content=[left_container, right_container])

Content can be specified when creating the widget, or after creation by assigning
the ``content`` attribute. The direction of the split can also be configured, either
at time of creation, or by setting the ``direction`` attribute:

.. code-block:: python

    import toga
    from toga.constants import Direction

    split = toga.SplitContainer(direction=Direction.HORIZONTAL)

    left_container = toga.Box()
    right_container = toga.ScrollContainer()

    split.content = [left_container, right_container]

By default, the space of the SplitContainer will be evenly divided between the
two panels. To specify an uneven split, you can provide a flex value when specifying
content. In the following example, there will be a 60/40 split between the left
and right panels.

.. code-block:: python

    import toga

    split = toga.SplitContainer()
    left_container = toga.Box()
    right_container = toga.ScrollContainer()

    split.content = [(left_container, 3), (right_container, 2)]

This only specifies the initial split; the split can be modified by the user
once it is displayed.

Reference
---------

.. autoclass:: toga.SplitContainer
   :exclude-members: HORIZONTAL, VERTICAL, window, app
