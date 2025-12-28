# Image format plugins

Extensions that enable Toga to understand additional image formats.

## Usage

Toga can be extended, via plugins, to understand externally defined image types, gaining the ability to convert them to and from its own [`toga.Image`][] class. Toga's [`Pillow`](https://pillow.readthedocs.io/en/stable/index.html) support is, in fact, implemented as a plugin that's included as part of the core Toga package.

An image format plugin consists of two things:

- a converter class conforming to the [`ImageConverter`][toga.images.ImageConverter] protocol, with methods defining how to convert to and from your image class
- an [entry point](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata) in the `toga.image_formats` group telling Toga the path to your converter class.

Let's say you want to tell Toga how to handle an image class called `MyImage`, and you're publishing your plugin as a package named `togax-myimage` (see [package prefixes][package-prefixes]) that contains a `plugins.py` module that defines your `MyImageConverter` plugin class. Your `pyproject.toml` might include something like the following:

```toml
[project.entry-points."toga.image_formats"]
myimage = "togax_myimage.plugins.MyImageConverter"
```

The variable name being assigned to (`myimage` in this case) can be whatever you like (although it should probably have some relationship to the image format name) What matters is the string assigned to it, which represents where Toga can find (and import) your [`ImageConverter`][toga.images.ImageConverter] class.

### Package prefixes

An image plugin can be registered from any Python module. If you maintain a package defining an image format, you could include a Toga converter plugin along with it. If you're publishing a plugin as a standalone package, you should title it with a `togax-` prefix, to indicate that it's an unofficial extension for Toga. Do *not* use the `toga-` prefix, as the BeeWare Project wishes to reserve that package prefix for "official" packages.

## Reference

Any class that represents an image.

::: toga.images.ImageConverter
