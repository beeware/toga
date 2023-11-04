ActivityIndicator
=================

A small animated indicator showing activity on a task of indeterminate length,
usually rendered as a "spinner" animation.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/activityindicator-cocoa.png
       :align: center
       :width: 100px

  .. group-tab:: Linux

    .. figure:: /reference/images/activityindicator-gtk.png
       :align: center
       :width: 100px

  .. group-tab:: Windows |no|

    Not supported

  .. group-tab:: Android |no|

    Not supported

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/activityindicator-web.png
    ..    :align: center
    ..    :width: 100px

    Screenshot not available

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

.. code-block:: python

    import toga

    indicator = toga.ActivityIndicator()

    # Start the animation
    indicator.start()

    # Stop the animation
    indicator.stop()

Notes
-----

* The ActivityIndicator will always take up a fixed amount of physical space in
  a layout. However, the widget will not be visible when it is in a "stopped"
  state.

Reference
---------

.. autoclass:: toga.ActivityIndicator
