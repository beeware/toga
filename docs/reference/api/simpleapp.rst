SimpleApp
=========

A base class for apps that have the minimum possible set of features for the platform.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(SimpleApp|Component))'}


Usage
-----

A SimpleApp is a specialized subclass of App that has the minimum possible set
of features for the platform.

A Toga :class:`~toga.App` generates a main window that has a menu bar, populated
with common commands and app features such as the ability to quit the app, an
About dialog, undo/redo, links to a project homepage, and so on.

However, for some applications, these menu items are not required. A SimpleApp
will generate the minimal app that is legal on a platform. The app will have a
main window, and closing that main window will exit the app. However, the main
window will not have a menu bar or any other default decorations. If the
platform *requires* a menu (e.g., on macOS, where the menu is tied to the app,
rather than the window), only the minimal commands required for HIG compliance
will be automatically added.

Reference
---------

.. autoclass:: toga.SimpleApp
   :members:
   :inherited-members:
   :undoc-members:
