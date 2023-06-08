ImageView
=========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(ImageView|Component)$)'}

A widget that displays an image.

Usage
-----

.. code-block:: python

    import toga

    my_image = toga.Image(self.paths.app / "brutus.png")
    view = toga.ImageView(my_image)

Notes
-----

* The default size of the view is the size of the image, or 0x0 if ``image`` is
  ``None``.

* If an explicit width or height is specified, the size of the image will be
  fixed in that axis. The image will be scaled to fit in the available space so
  that the entire image can be seen, while preserving the aspect ratio of the
  image.

* If an explicit width *and* height is specified, the image will be scaled to
  fill the described size without preserving the aspect ratio.

* If an image is is given a style of ``flex=1``, it will be allowed to expand
  or contract in any axis that doesn't have an explicit size set. The aspect
  ratio of the image will be preserved during this scaling.

Reference
---------

.. autoclass:: toga.widgets.imageview.ImageView
   :members:
   :undoc-members:
