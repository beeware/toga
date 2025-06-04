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

* On iOS, style directives for changing the widget's color and background color will
  be ignored. Apple advises against customizing the look and feel of date pickers; as
  a result, they don't expose APIs to change the color of date widgets.

Reference
---------

.. autoclass:: toga.DateInput

.. autoprotocol:: toga.widgets.dateinput.OnChangeHandler
