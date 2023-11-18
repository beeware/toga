SplitContainer
==============

A container that divides an area into two panels with a movable border.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/splitcontainer-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/splitcontainer-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/splitcontainer-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android |no|

    Not supported

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

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
