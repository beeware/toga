MultilineTextInput
==================

A scrollable panel that allows for the display and editing of multiple lines of text.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/multilinetextinput-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/multilinetextinput-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/multilinetextinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/multilinetextinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/multilinetextinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

.. code-block:: python

    import toga

    textbox = toga.MultilineTextInput()
    textbox.value = "Some text.\nIt can be multiple lines of text."

The input can be provided a placeholder value - this is a value that will be
displayed to the user as a prompt for appropriate content for the widget. This
placeholder will only be displayed if the widget has no content; as soon as
a value is provided (either by the user, or programmatically), the placeholder
content will be hidden.

Notes
-----

* Winforms does not support the use of partially or fully transparent colors
  for the MultilineTextInput background. If a color with an alpha value is
  provided (including ``TRANSPARENT``), the alpha channel will be ignored.
  A ``TRANSPARENT`` background will be rendered as white.

Reference
---------

.. autoclass:: toga.MultilineTextInput
