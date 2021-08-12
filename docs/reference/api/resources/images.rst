Image
=====

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Image|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16


An image is graphical content of arbitrary size.

A Toga icon is a **late bound** resource - that is, it can be constructed
without an implementation. When it is assigned to an ImageView, or other
role where an Image is required, it is bound to a factory, at which time
the implementation is created.

The path specified for an Image can be:

1. A path relative to the module that defines your Toga application.
2. An absolute filesystem path
3. A URL. The content of the URL will be loaded in the background.

If the path specified does not exist, or cannot be loaded, a
``FileNotFoundError`` will be raised.

Usage
-----

Reference
---------

.. autoclass:: toga.images.Image
   :members:
   :undoc-members:
   :inherited-members:
