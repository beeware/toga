# ImageView

Test app for the
[ImageView widget](https://toga.beeware.org/en/stable/reference/api/widgets/imageview.html).

The top image view has an image loaded from a local path using
`toga.Image()`. No style parameters are applied.

The next two image views have an image loaded using a `pathlib.Path`
object, using `toga.Image()`. The first has width set, the second has
height set. Aspect ratio should be retained on both.

The next three image views have images passed directly to `ImageView()`,
the first using a relative path, and the final two using a
`pathlib.Path` object.

The first of these is styled with both width and height, and the aspect
ratio should be overridden.

The second is styled flex with an unspecified cross axis size, and the
aspect ratio should be retained.

The third is styled with flex with a fixed cross axis size, and the
aspect ratio should be retained.

The bottom image view is generated using PIL. It will render as a light
gray rectangle with the words "Pillow image" on it in green text.

## Quickstart

To run this example:

```
$ python -m pip install toga
$ python -m imageview
```
