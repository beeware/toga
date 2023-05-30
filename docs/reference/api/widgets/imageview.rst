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

Reference
---------

.. autoclass:: toga.widgets.imageview.ImageView
   :members:
   :undoc-members:
