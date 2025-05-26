DateInput
=========

A widget to select a calendar date.

.. tabs::

  .. group-tab:: macOS |no|

    Not supported

  .. group-tab:: Linux |no|

    Not supported

  .. group-tab:: Windows

    .. figure:: /reference/images/dateinput-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/dateinput-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/dateinput-iOS.png
       :align: center
       :width: 300px

  .. group-tab:: Web

    .. figure:: /reference/images/dateinput-web.png
       :align: center
       :width: 300px

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

.. code-block:: python

    import toga

    current_date = toga.DateInput()

Notes
-----

* This widget supports years from 1800 to 8999 inclusive.

* Properties that return :any:`datetime.date` objects can also accept:

  * :any:`datetime.datetime`: The date portion will be extracted.
  * :any:`str`: Will be parsed as an ISO8601 format date string (e.g., "2023-12-25").

* On iOS, setting its color sets its *tint color*, which is like an accent color for the date input, but it does
  not change the color of the date text because of limitations with iOS APIs that works across supported versions.

Reference
---------

.. autoclass:: toga.DateInput

.. autoprotocol:: toga.widgets.dateinput.OnChangeHandler
