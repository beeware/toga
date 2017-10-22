:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Matrix
============

Defines the transformation from user-space to device-space coordinates

Usage
-----

.. code-block:: Python

    import toga

    matrix = toga.Matrix(xx=1.0, yx=0.0, xy=0.0, yy=1.0, x0=0.0, y0=0.0)
    matrix.transform_point(10, 10)

Supported Platforms
-------------------

.. include:: ../supported_platforms/Matrix.rst

Reference
---------

.. autoclass:: toga.widgets.matrix.Matrix
:members:
       :undoc-members:
       :inherited-members:
