# Image

Graphical content of arbitrary size.

::: {.rst-class}
widget-support
:::

::: {.csv-filter header-rows="1" file="../../data/widgets_by_platform.csv" included_cols="4,5,6,7,8,9,10" include="{0: '^Image$'}"}
Availability (`Key <api-status-key>`{.interpreted-text role="ref"})
:::

## Usage

::: {.admonition}
Images and Icons are *not* the same!

Toga draws a distinction between an *Image* and an *Icon*. An
`~toga.Image`{.interpreted-text role="class"} can have an arbitrary size
or aspect ratio, and is *not* platform dependent - the same image will
be used on *every* platform. An Image is *not* an interactive element,
because there is no visual cue to the user that the image *can* be
interacted with.

An `~toga.Icon`{.interpreted-text role="class"}, on the other hand, is
small, square, and might vary between platforms. It is a visual element
that is often used as part of an interactive element such as a button, a
toolbar item, or a tab selector - but the Icon *itself* isn't an
interactive element.

If you are looking for a widget that the user can click on, you're
looking for a widget configured to use an Icon (probably
`~toga.Button`{.interpreted-text role="class"}), *not* an `on_press`
handler on an `~toga.Image`{.interpreted-text role="class"} or
`~toga.ImageView`{.interpreted-text role="class"}.
:::

An image can be constructed from a
`wide range of sources <ImageContentT>`{.interpreted-text role="any"}:

``` python
from pathlib import Path
import toga

# Load an image in the same folder as the file that declares the App class
my_image = toga.Image("brutus.png")

# Load an image at an absolute path
my_image = toga.Image(Path.home() / "path/to/brutus.png")

# Create an image from raw data
with (Path.home() / "path/to/brutus.png").open("rb") as f:
    my_image = toga.Image(data=f.read())

# Create an image from a PIL image (if PIL is installed)
import PIL.Image
my_pil_image = PIL.Image.new("L", (30, 30))
my_toga_image = toga.Image(my_pil_image)
```

You can also tell Toga how to convert from (and to) other classes that
represent images via
`image format plugins </reference/plugins/image_formats>`{.interpreted-text
role="doc"}.

## Notes

::: {#known-image-formats}
- PNG and JPEG formats are guaranteed to be supported. Other formats are
  available on some platforms:
  - GTK: BMP
  - macOS: GIF, BMP, TIFF
  - Windows: GIF, BMP, TIFF
:::

::: {#native-image-rep}
- The native platform representations for images are:
  - Android: `android.graphics.Bitmap`
  - GTK: `GdkPixbuf.Pixbuf`
  - iOS: `UIImage`
  - macOS: `NSImage`
  - Windows: `System.Drawing.Image`
:::

::: {#toga_image_subclassing}
- If you subclass `Image`{.interpreted-text role="any"}, you can supply
  that subclass as the requested format to any `as_format()` method in
  Toga, provided that your subclass has a constructor signature
  compatible with the base `Image`{.interpreted-text role="any"} class.
:::

## Reference

> When specifying content for an `Image`{.interpreted-text role="any"},
> you can provide:
>
> - a string specifying an absolute or relative path to a file in a
>   `known image
>   format <known-image-formats>`{.interpreted-text role="ref"};
> - an absolute or relative `~pathlib.Path`{.interpreted-text
>   role="class"} object describing a file in a
>   `known image format <known-image-formats>`{.interpreted-text
>   role="ref"};
> - a "blob of bytes" data type (`bytes`{.interpreted-text role="any"},
>   `bytearray`{.interpreted-text role="any"}, or
>   `memoryview`{.interpreted-text role="any"}) containing raw image
>   data in a
>   `known image format <known-image-formats>`{.interpreted-text
>   role="ref"};
> - an instance of `toga.Image`{.interpreted-text role="any"};
> - if [Pillow](https://pillow.readthedocs.io/) is installed, an
>   instance of `PIL.Image.Image`{.interpreted-text role="any"};
> - an image of a class registered via an `image format plugin
>   </reference/plugins/image_formats>`{.interpreted-text role="doc"}
>   (or a subclass of such a class); or
> - an instance of the
>   `native platform image representation <native-image-rep>`{.interpreted-text
>   role="ref"}.
>
> If a relative path is provided, it will be anchored relative to the
> module that defines your Toga application class.

::: {.autoclass}
toga.Image
:::
