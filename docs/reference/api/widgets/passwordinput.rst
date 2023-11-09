PasswordInput
=============

A widget to allow the entry of a password. Any value typed by the user will be
obscured, allowing the user to see the number of characters they have typed, but
not the actual characters.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/passwordinput-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/passwordinput-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/passwordinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/passwordinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/passwordinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

The ``PasswordInput`` is functionally identical to a :class:`~toga.TextInput`, except
for how the text is displayed. All features supported by :class:`~toga.TextInput` are
also supported by PasswordInput.

.. code-block:: python

    import toga

    password = toga.PasswordInput()

Notes
-----

* Winforms does not support the use of partially or fully transparent colors for
  the PasswordInput background. If a color with an alpha value is provided
  (including ``TRANSPARENT``), the alpha channel will be ignored. A
  ``TRANSPARENT`` background will be rendered as white.

* On Winforms, if a PasswordInput is given an explicit height, the rendered
  widget will not expand to fill that space. The widget will have the fixed
  height determined by the font used on the widget. In general, you should avoid
  setting a ``height`` style property on PasswordInput widgets.

Reference
---------

.. autoclass:: toga.PasswordInput
