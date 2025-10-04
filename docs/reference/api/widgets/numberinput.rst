NumberInput
===========

A text input that is limited to numeric input.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/numberinput-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/numberinput-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/numberinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/numberinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/numberinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web

    .. figure:: /reference/images/numberinput-web.png
       :align: center
       :width: 300px

  .. group-tab:: Textual

    .. figure:: /reference/images/numberinput-textual.png
       :align: center
       :width: 300px

Usage
-----

.. code-block:: python

    import toga

    widget = toga.NumberInput(min=1, max=10, step=0.001)
    widget.value = 2.718

NumberInput's properties can accept :class:`~decimal.Decimal`, :any:`int`, :any:`float`,
or :any:`str` containing numbers, but they always return :class:`~decimal.Decimal`
objects to ensure precision is retained.

Reference
---------

.. autoclass:: toga.NumberInput

.. autoprotocol:: toga.widgets.numberinput.OnChangeHandler
