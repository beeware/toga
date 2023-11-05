WindowlessApp
=============

An app that doesn't use a window as the primary user interface.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(WindowlessApp|Component))'}


Usage
-----

A WindowlessApp is a specialized subclass of App that is used for apps that *don't* have
a main window, such as an app that generates a icon in the system tray or status bar.
As there is no main window controlling the app, the app is responsible for defining the
user action that will exit the app.

Reference
---------

.. autoclass:: toga.WindowlessApp
   :members:
   :inherited-members:
   :undoc-members:
