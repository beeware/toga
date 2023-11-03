TimeInput
=========

A widget to select a clock time.

.. tabs::

  .. group-tab:: macOS |no|

    Not supported

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

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |no|

    Not supported

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

  * On Android, seconds will also be returned as zero.

* Properties that return :any:`datetime.time` objects can also accept:

  * :any:`datetime.datetime`: The time portion will be extracted.
  * :any:`str`: Will be parsed as an ISO8601 format time string (e.g., "06:12").


Reference
---------

.. autoclass:: toga.TimeInput
