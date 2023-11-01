Switch
======

A clickable button with two stable states: True (on, checked); and False (off,
unchecked). The button has a text label.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/switch-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/switch-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/switch-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/switch-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/switch-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/switch-web.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

.. code-block:: python

    import toga

    switch = toga.Switch()

    # What is the current state of the switch?
    print(f"The switch is {switch.value}")

Notes
-----

* The button and the label are considered a single widget for layout purposes.

* The visual appearance of a Switch is not guaranteed. On some platforms, it
  will render as a checkbox. On others, it will render as a physical "switch"
  whose position (and color) indicates if the switch is active. When rendered as
  a checkbox, the label will appear to the right of the checkbox. When rendered
  as a switch, the label will be left-aligned, and the switch will be
  right-aligned.

* You should avoid setting a ``height`` style property on Switch widgets. The
  rendered height of the Switch widget will be whatever the platform style guide
  considers appropriate; explicitly setting a ``height`` for the widget can
  lead to widgets that have a distorted appearance.

* On macOS, the text color of the label cannot be set directly; any ``color`` style
  directive will be ignored.

Reference
---------

.. autoclass:: toga.Switch
