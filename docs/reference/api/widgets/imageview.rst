ImageView
=========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
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

* If an explicit width *or* height is specified, the size of the image will be fixed in
  that axis, and the size in the other axis will be determined by the image's aspect
  ratio.

* If an explicit width *and* height is specified, the image will be scaled to fill the
  described size without preserving the aspect ratio.

* If an ImageView is given a style of ``flex=1``, and doesn't have an explicit size set
  along its container's main axis, it will be allowed to expand and contract along that
  axis.

  * If the cross axis size is unspecified, it will be determined by the image's aspect
    ratio, with a minimum size in the main axis matching the size of the image in the
    main axis.

  * If the cross axis has an explicit size, the image will be scaled to fill the
    available space so that the entire image can be seen, while preserving its aspect
    ratio. Any extra space will be distributed equally between both sides.


Reference
---------

.. autoclass:: toga.ImageView
