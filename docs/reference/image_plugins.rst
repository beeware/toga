============================================
Registering external image types via plugins
============================================


Usage
~~~~~

Toga can be extended, via plugins, to understand externally defined image types, gaining
the ability to convert them to and from its own :any:`toga.Image` class.

A plugin defining how to handle an image format must define three things:

* ``image_class``

  The class representing an image that we want to tell Toga about. For our example, it
  would be assigned ``MyImage``. (You will, of course, have to import the relevant
  class in order to refer to it.)

* ``convert_from_format(image_in_format)``

  This top-level function should accept an image of the relevant image class, and return a
  bytes-like object representing the image in PNG format.

* ``convert_to_format(data, image_class=None)``

  This top-level function should accept a bytes-like object representing the image in PNG
  format, and return an instance of the image class in question. Assuming your image
  class meaningfully supports subclassing, if a subclass is provided as ``image_class``,
  you should return an instance of that subclass instead. (This assumes the subclass's
  initializer has a compatible signature.)


These can be accessible from directly importing your package, or in a
submodule/subpackage. Wherever they are, you need to tell Toga via an `entry point`_ in
your metadata.

Let's say you want to tell Toga how to handle an image class called ``MyImage``. You
could include the necessary converter in the library defining ``MyImage``, but let's
say you're not the maintainer, so you're making a separate package. Third-party
packages intended to extend Toga are recommended to start with the prefix ``togax_``
(``toga_`` being reserved for official packages maintained by BeeWare), so you might
name your package ``togax_myimage``. Let's also say you've defined ``image_class``,
``convert_from_format``, and ``convert_to_format`` in a file named ``converter.py`` in
that package.

Then in your ``pyproject.toml`` you would include the following:

.. code-block:: toml

    [project.entry-points."toga.image_formats"]
    myimage = "togax_myimage.converter"

The name of the value doesn't matter in this case, only its *value*, which should be
string representing whatever module or package name Toga can import to get the
necessary definitions.


.. _entry point: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata
