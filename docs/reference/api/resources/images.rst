Image
=====

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Image|Component)$)'}


An image is graphical content of arbitrary size.

An image can be constructed using:

1. A path relative to the module that defines your Toga application. (either as
   a string, or as a :any:`pathlib.Path` object)
2. An absolute file system path (either as a string, or as a :any:`pathlib.Path`
   object)
3. Raw binary image data.

If the path specified does not exist, or cannot be loaded, a
``FileNotFoundError`` will be raised.

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


Reference
---------

.. autoclass:: toga.images.Image
   :members:
   :undoc-members:
