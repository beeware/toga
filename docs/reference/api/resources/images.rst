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

.. admonition:: Images and Icons are *not* the same!

    Toga draws a distinction between an *Image* and an *Icon*. An :class:`~toga.Image`
    can have an arbitrary size or aspect ratio, and is *not* platform dependent - the
    same image will be used on *every* platform. An Image is *not* an interactive
    element, because there is no visual cue to the user that the image *can* be
    interacted with.

    An :class:`~toga.Icon`, on the other hand, is small, square, and might vary between
    platforms. It is a visual element that is often used as part of an interactive
    element such as a button, a toolbar item, or a tab selector - but the Icon *itself*
    isn't an interactive element.

    If you are looking for a widget that the user can click on, you're looking for a
    widget configured to use an Icon (probably :class:`~toga.Button`), *not* an
    ``on_press`` handler on an :class:`~toga.Image` or :class:`~toga.ImageView`.

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

You can also tell Toga how to convert from (and to) other classes that represent images
via :doc:`image format plugins </reference/plugins/image_plugins>`.

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

.. _toga_image_subclassing:

* If you subclass :any:`Image`, you can supply that subclass as the requested
  format to :any:`Image.as_format`. If you do, make sure that your subclass has a compatible
  constructor signature, as Toga will attempt to create it the same way as it would a
  base :any:`Image`.

  The same consideration applies when providing such a subclass as the format argument to:

  - :any:`Canvas.as_image`
  - :any:`ImageView.as_image`
  - :any:`Screen.as_image`
  - :any:`Window.as_image`

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
    * an instance of :any:`toga.Image`;
    * if `Pillow <https://pillow.readthedocs.io/>`_ is installed, an instance of
      :any:`PIL.Image.Image`;
    * an image of a class registered via an :doc:`image format plugin
      </reference/plugins/image_plugins>` (or a subclass of such a class); or
    * an instance of the :ref:`native platform image representation <native-image-rep>`.

    If a relative path is provided, it will be anchored relative to the module that
    defines your Toga application class.

.. autoclass:: toga.Image
