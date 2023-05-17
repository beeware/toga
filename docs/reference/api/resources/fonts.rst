Font
====

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Font|Component))'}

The font class is used for abstracting the platforms implementation of fonts.

Notes
-----

* Windows does not support the use of the Oblique font style. A request for an
  oblique font will be interpreted as Italic.

* Windows does not support the use of a Small Caps variant on fonts. A request
  for a Small Caps variant will be ignored.

Reference
---------

.. autoclass:: toga.fonts.Font
   :members:
   :undoc-members:
