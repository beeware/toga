{{ component_header("Image") }}

## Usage

/// admonition | Images and Icons are *not* the same!

Toga draws a distinction between an *Image* and an *Icon*. An [`Image`][toga.Image] can have an arbitrary size or aspect ratio, and is *not* platform dependent - the same image will be used on *every* platform. An Image is *not* an interactive element, because there is no visual cue to the user that the image *can* be interacted with.

An [`Icon`][toga.Icon], on the other hand, is small, square, and might vary between platforms. It is a visual element that is often used as part of an interactive element such as a button, a toolbar item, or a tab selector - but the Icon *itself* isn't an interactive element.

If you are looking for a widget that the user can click on, you're looking for a widget configured to use an Icon (probably [`Button`][toga.Button]), *not* an `on_press` handler on an [`Image`][toga.Image] or [`ImageView`][toga.ImageView].

///

An image can be constructed from a
[wide range of sources][toga.images.ImageContentT]:

```python
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

You can also tell Toga how to convert from (and to) other classes that represent images via [image format plugins](image-format-plugins.md).

## Notes

[](){ #known-image-formats }

- PNG and JPEG formats are guaranteed to be supported. Other formats are available on some platforms:
    - GTK: BMP
    - macOS: GIF, BMP, TIFF
    - Windows: GIF, BMP, TIFF

[](){ #native-image-rep }

- The native platform representations for images are:
    - Android: `android.graphics.Bitmap`
    - GTK: `GdkPixbuf.Pixbuf`
    - iOS: `UIImage`
    - macOS: `NSImage`
    - Windows: `System.Drawing.Image`

[](){ #toga_image_subclassing }

- If you subclass [`toga.Image`][], you can supply that subclass as the requested format to any `as_format()` method in Toga, provided that your subclass has a constructor signature compatible with the base [`toga.Image`][] class.

## Reference

::: toga.Image

::: toga.images.ImageContentT

::: toga.images.ImageT

::: toga.images.ExternalImageT
