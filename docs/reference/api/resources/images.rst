Image
=====

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Image|Component)$)'}


An image is graphical content of arbitrary size.

Usage
-----

.. code-block:: python

    from pathlib import Path
    import toga

    # Load an image in the same folder as the file that declares the App class
    my_image = toga.Image("brutus.png")

    # Load an image at an absolute path
    my_image = toga.Image(Path.home() / "path" / "to" / "brutus.png")

    # Create an image from raw data
    with (Path.home() / "path" / "to" / "brutus.png").open("rb") as f:
        my_image = toga.Image(data=f.read())

Notes
-----

* PNG and JPEG formats are guaranteed to be supported.
  Other formats are available on some platforms:

  - macOS: GIF, BMP, TIFF
  - GTK: BMP
  - Windows: GIF, BMP, TIFF

Reference
---------

.. autoclass:: toga.Image
