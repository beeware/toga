Image
=====

Graphical content of arbitrary size.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Image|Component)$)'}

Usage
-----

An image can be constructed from a :any:`wide range of sources <ImageContent>`:

.. code-block:: python

    from pathlib import Path
    import toga

    # Load an image in the same folder as the file that declares the App class
    my_image = toga.Image("brutus.png")

    # Load an image at an absolute path
    my_image = toga.Image(Path.home() / "path/to/brutus.png")

    # Create an image from raw data
    with (Path.home() / "path/to/brutus.png").open("rb") as f:
        my_image = toga.Image(data=f.read())

    # Create an image from a PIL image (if PIL is installed)
    import PIL.Image
    my_pil_image = PIL.Image.new("L", (30, 30))
    my_toga_image = toga.Image(my_pil_image)

Notes
-----

.. _known-image-formats:

* PNG and JPEG formats are guaranteed to be supported.
  Other formats are available on some platforms:

  - GTK: BMP
  - macOS: GIF, BMP, TIFF
  - Windows: GIF, BMP, TIFF

.. _native-image-rep:

* The native platform representations for images are:

  - Android: ``android.graphics.Bitmap``
  - GTK: ``GdkPixbuf.Pixbuf``
  - iOS: ``UIImage``
  - macOS: ``NSImage``
  - Windows: ``System.Drawing.Image``

Reference
---------

.. c:type:: ImageContent

    When specifying content for an :any:`Image`, you can provide:

    * a string specifying an absolute or relative path to a file in a :ref:`known image
      format <known-image-formats>`;
    * an absolute or relative :any:`pathlib.Path` object describing a file in a
      :ref:`known image format <known-image-formats>`;
    * a "blob of bytes" data type (:any:`bytes`, :any:`bytearray`, or :any:`memoryview`)
      containing raw image data in a :ref:`known image format <known-image-formats>`;
    * an instance of :any:`toga.Image`; or
    * if `Pillow <https://pillow.readthedocs.io/>`__ is installed, an instance of
      :any:`PIL.Image.Image`; or
    * an instance of the :ref:`native platform image representation <native-image-rep>`.

    If a relative path is provided, it will be anchored relative to the module that
    defines your Toga application class.

.. autoclass:: toga.Image
