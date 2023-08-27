TimeInput
=========

A widget to select a clock time.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/timeinput-macOS.png
       :align: center

  .. group-tab:: Linux

    .. figure:: /reference/images/timeinput-gtk.png
       :align: center

  .. group-tab:: Windows

    .. figure:: /reference/images/timeinput-winforms.png
       :align: center

  .. group-tab:: Android

    .. figure:: /reference/images/timeinput-android.png
       :align: center

  .. group-tab:: iOS

    .. figure:: /reference/images/timeinput-ios.png
       :align: center


.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(TimeInput|Component))'}

Usage
-----

.. code-block:: python

    import toga

    current_time = toga.TimeInput()

Notes
-----

* This widget supports hours, minutes and seconds. Microseconds will always be returned
  as zero.

  * On Android, seconds will also be returned as zero.

* Properties that return :any:`datetime.time` objects can also accept:

  * :any:`datetime.datetime`: The time portion will be extracted.
  * :any:`str`: Will be parsed as an ISO8601 format time string (e.g., "06:12").


Reference
---------

.. autoclass:: toga.TimeInput
