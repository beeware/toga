Icon
====

A small, square image, used to provide easily identifiable visual context to a widget.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Icon|Component))'}

Usage
-----

The filename specified for an icon should be specified *without* an extension; the
platform will determine an appropriate extension, and may also modify the name of the
icon to include a size qualifier.

The following formats are supported (in order of preference):

* **Android** - PNG
* **iOS** - ICNS, PNG, BMP, ICO
* **macOS** - ICNS, PNG, PDF
* **GTK** - PNG, ICO, ICNS. 32px and 72px variants of each icon can be provided;
* **Windows** - ICO, PNG, BMP

The first matching icon of the most specific size will be used. For example, on Windows,
specifying an icon of ``myicon`` will cause Toga to look for ``myicon.ico``, then
``myicon.png``, then ``myicon.bmp``. On GTK, Toga will look for ``myicon-72.png`` and
``myicon-32.png``, then ``myicon.png``, then ``myicon-72.ico`` and ``myicon-32.ico``, and so on.

An icon is **guaranteed** to have an implementation. If you specify a path and no
matching icon can be found, Toga will output a warning to the console, and load a
default "Tiberius the yak" icon.

Reference
---------

.. autoclass:: toga.Icon
