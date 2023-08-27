DateInput
=========

A widget to select a calendar date.

.. tabs::

  .. group-tab:: macOS

    Not supported
    .. .. figure:: /reference/images/dateinput-macOS.png
    ..    :align: center

  .. group-tab:: Linux

    Not supported
    .. .. figure:: /reference/images/dateinput-gtk.png
    ..    :align: center

  .. group-tab:: Windows

    .. figure:: /reference/images/dateinput-winforms.png
       :align: center

  .. group-tab:: Android

    .. figure:: /reference/images/dateinput-android.png
       :align: center

  .. group-tab:: iOS

    Not supported
    .. .. figure:: /reference/images/dateinput-ios.png
    ..    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(DateInput|Component))'}

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

Reference
---------

.. autoclass:: toga.DateInput
