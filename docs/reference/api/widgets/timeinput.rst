TimeInput
=========

A widget to select a clock time.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/timeinput-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux |no|

    Not supported

  .. group-tab:: Windows

    .. figure:: /reference/images/timeinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/timeinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/timeinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web |no|

    .. figure:: /reference/images/timeinput-web.png
       :align: center
       :width: 300px

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

.. code-block:: python

    import toga

    current_time = toga.TimeInput()

Notes
-----

* This widget supports hours, minutes and seconds. Microseconds will always be returned
  as zero.

  * On Android and iOS, seconds will also be returned as zero, and any second component of a minimum or maximum value will be ignored.

* Properties that return :any:`datetime.time` objects can also accept:

  * :any:`datetime.datetime`: The time portion will be extracted.
  * :any:`str`: Will be parsed as an ISO8601 format time string (e.g., "06:12").


Reference
---------

.. autoclass:: toga.TimeInput

.. autoprotocol:: toga.widgets.timeinput.OnChangeHandler
