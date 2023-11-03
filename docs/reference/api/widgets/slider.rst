Slider
======

A widget for selecting a value within a range. The range is shown as a horizontal line,
and the selected value is shown as a draggable marker.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/slider-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/slider-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/slider-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/slider-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/slider-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported


Usage
-----

A slider can either be continuous (allowing any value within the range), or discrete
(allowing a fixed number of equally-spaced values). For example:

.. code-block:: python

    import toga

    def my_callback(slider):
        print(slider.value)

    # Continuous slider, with an event handler.
    toga.Slider(range=(-5, 10), value=7, on_change=my_callback)

    # Discrete slider, accepting the values [0, 1.5, 3, 4.5, 6, 7.5].
    toga.Slider(range=(0, 7.5), tick_count=6)


Reference
---------

.. autoclass:: toga.Slider
