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

  .. group-tab:: Windows

    .. figure:: /reference/images/activityindicator-winforms.png
       :align: center
       :width: 100px

  .. group-tab:: Android

    .. figure:: /reference/images/activityindicator-android.png
       :align: center
       :width: 100px

  .. group-tab:: iOS

    .. figure:: /reference/images/activityindicator-iOS.png
       :align: center
       :width: 100px

  .. group-tab:: Web |beta|

    .. figure:: /reference/images/activityindicator-web.png
       :align: center
       :width: 100px

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
* On iOS, Android, and WinForms, the background color of the widget itself may
  not be drawn when the widget is in a stopped state.  In general, it is not
  recommended to have a non-transparent background color on the spinner itself.

Reference
---------

.. autoclass:: toga.ActivityIndicator
