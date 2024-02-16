====================
Image Format Plugins
====================


Usage
~~~~~

Toga can be extended, via plugins, to understand externally defined image types, gaining
the ability to convert them to and from its own :any:`Image` class. Toga's `Pillow`_
support, in fact, is implemented as a plugin that's included as part of the core Toga
package.

An image format plugin consists of two things:

- a converter class conforming to the :any:`ImageConverter` protocol, with methods
  defining how to convert to and from your image class
- an `entry point`_ in your metadata telling Toga where to find your converter class


The entry point should be listed in the ``"toga.image_formats"`` group. Let's say you
want to tell Toga how to handle an image class called ``MyImage``, and you're
publishing your plugin as a package named ``togax-myimage`` (see :ref:`package prefixes
<package_prefixes>`). Your ``pyproject.toml`` might include something like the
following:

.. code-block:: toml

    [project.entry-points."toga.image_formats"]
    myimage = "togax_myimage.MyImageConverter"

The variable name being assigned to (``myimage`` in this case) can be whatever you like.
What matters is the string assigned to it, which represents where Toga can find
(and import) your :any:`ImageConverter` class.

Notes
~~~~~

.. _package_prefixes:

- An image plugin can be registered from anywhere; if you maintain a package defining an
  image format, you could include a Toga converter plugin along with it. If you're
  publishing a plugin as a standalone package, you may want to title it with a
  ``togax-`` prefix, to indicate that it's an unofficial extension for Toga. (We want to
  reserve the ``toga-`` prefix for "official" packages.)

.. _external_image_subclassing:

- By default, Toga will assume any subclass of your image class can be created
  (and converted from) in the same way as the base class. If a subclass needs special
  treatment (e.g. if it has an incompatible constructor), you can create a separate
  converter for it. Your converter entry points should be ordered from most to least
  specific. In other words, you probably want:

  .. code-block:: toml

    [project.entry-points."toga.image_formats"]
    myimage_subclass = "togax_myimage.MyImageSubclassConverter"
    myimage = "togax_myimage.MyImageConverter"

  If the base class's converter is listed first, the subclass converter will never be
  used.




Reference
~~~~~~~~~

.. autoprotocol:: toga.images.ImageConverter


.. _entry point: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata

.. _Pillow: https://pillow.readthedocs.io/en/stable/index.html
