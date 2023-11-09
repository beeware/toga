TextInput
=========

A widget for the display and editing of a single line of text.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/textinput-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/textinput-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/textinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/textinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/textinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/textinput-web.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

  .. group-tab:: Textual |beta|

    .. .. figure:: /reference/images/textinput-textual.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

Usage
-----

.. code-block:: python

    import toga

    text_input = toga.TextInput()
    text_input.value = "Jane Developer"

The input can be provided a placeholder value - this is a value that will be
displayed to the user as a prompt for appropriate content for the widget. This
placeholder will only be displayed if the widget has no content; as soon as
a value is provided (either by the user, or programmatically), the placeholder
content will be hidden.

The input can also be provided a list of :ref:`validators <validators>`. A
validator is a function that will be invoked whenever the content of the input
changes. The function should return ``None`` if the current value of the input
is valid; if the current value is invalid, it should return an error message.

Notes
-----

* Although an error message is provided when validation fails, Toga does not
  guarantee that this error message will be displayed to the user.

* Winforms does not support the use of partially or fully transparent colors for
  the TextInput background. If a color with an alpha value is provided
  (including ``TRANSPARENT``), the alpha channel will be ignored. A
  ``TRANSPARENT`` background will be rendered as white.

* On Winforms, if a TextInput is given an explicit height, the rendered widget
  will not expand to fill that space. The widget will have the fixed height
  determined by the font used on the widget. In general, you should avoid
  setting a ``height`` style property on TextInput widgets.

Reference
---------

.. autoclass:: toga.TextInput
