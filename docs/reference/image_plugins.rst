============================================
Registering external image types via plugins
============================================


Usage
~~~~~

Toga can be extended, via plugins, to understand externally defined image types, gaining
the ability to convert them to and from its own :any:`toga.Image` class.


To create an image format plugin that Toga will recognize, make a Python package whose
name starts with the prefix ``togax_``. (The ``toga_`` prefix is intended for *official*
packages maintained by BeeWare.) Then include `metadata`_ exposing an entry point
for "toga.image_formats", with your package's name as its value. For example, if you
have an image class called ``MyImage``, you might name your package ``togax_myimage``,
and then your ``pyproject.toml`` would include the following:

.. code-block:: toml

    [project.entry-points."toga.image_formats"]
    myimage = "togax_myimage"

The name of the value doesn't matter in this case, only its *value*, which should be the
same as the name of your plugin package.

The only other (Toga-specific) thing your package needs to include is a file named
``converter.py``, which must define three things:

``image_class``
----------------

The class representing an image that we want to tell Toga about. For our example, it
would be assigned ``MyImage``. (You will, of course, have to import the relevant class in order to
refer to it.)

``convert_from_format(image_in_format)``
----------------------------------------

This top-level function should accept an image of the relevant image class, and return a
bytes-like object representing the image in PNG format.


``convert_to_format(data, image_format=None)``
----------------------------------------------

This top-level function should accept a bytes-like object representing the image in PNG
format, and return an instance of the image class in question. Assuming your image
class meaningfully supports subclassing, if a subclass is provided as ``image_format``,
you should return an instance of that subclass instead. (This assumes the subclass's
initializer has a compatible signature.)


Example
~~~~~~~

Toga itself includes one image format plugin, for converting to and from
Pillow's :any:`PIL.Image.Image`. You can look at its `source` for an
example of how it's implemented.

A quirk of this particular plugin is that it's automatically installed with Toga, but a
given user may or may not have Pillow installed. So the plugin has to have a safety
check to confirm Pillow is available, and disable itself otherwise. This shouldn't
normally be necessary in your own image plugin, because it would only be installed
alongside the relevant image library (and if that weren't available, you'd
probably *want* an error telling you so).

.. _metadata: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata
.. _source: https://github.com/beeware/toga/tree/main/pil/
