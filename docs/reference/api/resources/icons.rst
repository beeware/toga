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

.. admonition:: Icons and Images are *not* the same!

    Toga draws a distinction between an *Icon* and an *Image*. An :class:`~toga.Icon` is
    small, square, and might vary between platforms. It is a visual element that is
    often used as part of an interactive element such as a button, toolbar item, or tab
    selector - but the Icon *itself* isn't an interactive element.

    An :class:`~toga.Image`, on the other hand, can have an arbitrary size or aspect
    ratio, and is *not* platform dependent - the same image will be used on *every*
    platform. An Image is *not* an interactive element, because there is no visual cue
    to the user that the image *can* be interacted with.

    If you are looking for a widget that the user can click on, you're looking for a
    widget configured to use an Icon (probably :class:`~toga.Button`), *not* an
    ``on_press`` handler on an :class:`~toga.Image` or :class:`~toga.ImageView`.

The filename specified for an icon should be specified *without* an extension; the
platform will determine an appropriate extension, and may also modify the name of the
icon to include a platform and/or size qualifier.

The following formats are supported (in order of preference):

* **Android** - PNG
* **iOS** - ICNS, PNG, BMP, ICO
* **macOS** - ICNS, PNG, PDF
* **GTK** - PNG, ICO, ICNS; 512, 256, 128, 72, 64, 32, and 16px variants of each icon
  can be provided;
* **Windows** - ICO, PNG, BMP

The first matching icon of the most specific platform, with the most specific
size will be used. For example, on Windows, specifying an icon of ``myicon``
will cause Toga to look for (in order):

* ``myicon-windows.ico``
* ``myicon.ico``
* ``myicon-windows.png``
* ``myicon.png``
* ``myicon-windows.bmp``
* ``myicon.bmp``

On GTK, Toga will perform this lookup for each variant size, falling back to a name
without a size specifier if a size-specific variant has not been provided. For example,
when resolving the 32px variant, Toga will look for (in order):

* ``myicon-linux-32.png``
* ``myicon-32.png``
* ``myicon-linux-32.ico``
* ``myicon-32.ico``
* ``myicon-linux-32.icns``
* ``myicon-32.icns``
* ``myicon.png``
* ``myicon.ico``

Any icon that is found will be resized to the required size. Toga will generate any GTK
icon variants that are not available from the highest resolution provided (e.g., if no
128px variant can be found, one will be created by scaling the highest resolution
variant that *is* available).

An icon is **guaranteed** to have an implementation, regardless of the path
specified. If you specify a path and no matching icon can be found, Toga will
output a warning to the console, and return :attr:`~toga.Icon.DEFAULT_ICON`.

Reference
---------

.. c:type:: IconContent

    When specifying an :any:`Icon`, you can provide:

    * a string specifying an absolute or relative path;
    * an absolute or relative :any:`pathlib.Path` object; or
    * an instance of :any:`toga.Icon`.

    If a relative path is provided, it will be anchored relative to the module that
    defines your Toga application class.

.. autoclass:: toga.Icon
