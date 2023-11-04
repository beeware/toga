Button
======

A button that can be pressed or clicked.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/button-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/button-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/button-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/button-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/button-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/button-web.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

  .. group-tab:: Textual |beta|

    .. .. figure:: /reference/images/button-textual.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

Usage
-----

A button has a text label. A handler can be associated with button press events.

.. code-block:: python

    import toga

    def my_callback(button):
        # handle event
        pass

    button = toga.Button("Click me", on_press=my_callback)

Notes
-----

* A background color of ``TRANSPARENT`` will be treated as a reset of the button
  to the default system color.

* On macOS, the button text color cannot be set directly; any ``color`` style
  directive will be ignored. The text color is automatically selected by
  the platform to contrast with the background color of the button.

Reference
---------

.. autoclass:: toga.Button

.. autoprotocol:: toga.widgets.button.OnPressHandler
