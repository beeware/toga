Icon
====

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Icon|Component))'}


Usage
-----

An icon is a small, square image, used to decorate buttons and menu items.

A Toga icon is a **late bound** resource - that is, it can be constructed
without an implementation. When it is assigned to an app, command, or other
role where an icon is required, it is bound to a factory, at which time
the implementation is created.

The filename specified for an icon is interpreted as a path relative to the
module that defines your Toga application. The only exception to this is a
system icon, which is relative to the toga core module itself.

An icon is **guaranteed** to have an implementation. If you specify a filename
that cannot be found, Toga will output a warning to the console, and load a
default icon.

When an icon file is specified, you can optionally omit the extension. If an
extension is provided, that literal file will be loaded. If the platform
backend cannot support icons of the format specified, the default icon will
be used. If an extension is *not* provided, Toga will look for a file with the
one of the platform's allowed extensions.

Reference
---------

.. autoclass:: toga.Icon
   :members:
   :undoc-members:
