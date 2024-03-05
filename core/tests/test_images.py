from pathlib import Path

import PIL.Image
import pytest

import toga
from toga_dummy.plugins.image_formats import (
    CustomImage,
    CustomImageSubclass,
    DisabledImageConverter,
)
from toga_dummy.utils import assert_action_performed_with

RELATIVE_FILE_PATH = Path("resources/sample.png")
ABSOLUTE_FILE_PATH = Path(__file__).parent / "resources/sample.png"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        # Fully qualified path
        ((ABSOLUTE_FILE_PATH,), {}),
        ((), {"src": ABSOLUTE_FILE_PATH}),
        ((), {"path": ABSOLUTE_FILE_PATH}),
        # Fully qualified string
        ((f"{ABSOLUTE_FILE_PATH}",), {}),
        ((), {"src": f"{ABSOLUTE_FILE_PATH}"}),
        ((), {"path": f"{ABSOLUTE_FILE_PATH}"}),
        # Relative path
        ((RELATIVE_FILE_PATH,), {}),
        ((), {"src": RELATIVE_FILE_PATH}),
        ((), {"path": RELATIVE_FILE_PATH}),
        # Relative string
        ((f"{RELATIVE_FILE_PATH}",), {}),
        ((), {"src": f"{RELATIVE_FILE_PATH}"}),
        ((), {"path": f"{RELATIVE_FILE_PATH}"}),
    ],
)
def test_create_from_file(app, args, kwargs):
    """An image can be constructed from a file."""
    image = toga.Image(*args, **kwargs)

    # Image is bound
    assert image._impl is not None
    # impl/interface round trips
    assert image._impl.interface == image

    # The image's path is fully qualified
    assert image._impl.interface.path == ABSOLUTE_FILE_PATH


MISSING_ABSOLUTE_PATH = Path.home() / "does/not/exist/image.jpg"
MISSING_RELATIVE_PATH = Path("does/not/exist/image.jpg")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        # Empty string
        (("",), {}),
        ((), {"src": ""}),
        # Absolute path
        ((MISSING_ABSOLUTE_PATH,), {}),
        ((), {"src": MISSING_ABSOLUTE_PATH}),
        ((), {"path": MISSING_ABSOLUTE_PATH}),
        # Absolute string
        ((f"{MISSING_ABSOLUTE_PATH}",), {}),
        ((), {"src": f"{MISSING_ABSOLUTE_PATH}"}),
        ((), {"path": f"{MISSING_ABSOLUTE_PATH}"}),
        # Relative path
        ((MISSING_RELATIVE_PATH,), {}),
        ((), {"src": f"{MISSING_RELATIVE_PATH}"}),
        ((), {"path": f"{MISSING_RELATIVE_PATH}"}),
        # Relative string
        ((f"{MISSING_RELATIVE_PATH}",), {}),
        ((), {"src": f"{MISSING_RELATIVE_PATH}"}),
        ((), {"path": f"{MISSING_RELATIVE_PATH}"}),
    ],
)
def test_create_with_nonexistent_file(app, args, kwargs):
    """If a file image source doesn't exist, an error is raised."""
    with pytest.raises(FileNotFoundError):
        toga.Image(*args, **kwargs)


BYTES = ABSOLUTE_FILE_PATH.read_bytes()


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        ((BYTES,), {}),
        ((), {"src": BYTES}),
        ((), {"data": BYTES}),
        # Other "lump of bytes" data types
        ((bytearray(BYTES),), {}),
        ((memoryview(BYTES),), {}),
    ],
)
def test_create_from_bytes(args, kwargs):
    """An image can be constructed from data."""
    image = toga.Image(*args, **kwargs)

    # Image is bound
    assert image._impl is not None
    # impl/interface round trips
    assert image._impl.interface == image

    # Image was constructed with data
    assert_action_performed_with(image, "load image data", data=BYTES)


def test_create_from_raw():
    """An image can be created from a raw data source."""
    orig = toga.Image(BYTES)

    copy = toga.Image(orig._impl.native)
    # Image is bound
    assert copy._impl is not None
    # impl/interface round trips
    assert copy._impl.interface == copy

    # Image was constructed from raw data
    assert_action_performed_with(copy, "load image from raw")


def test_no_source():
    """If no source is provided, an error is raised."""
    with pytest.raises(
        TypeError,
        match=r"Image.__init__\(\) missing 1 required positional argument: 'src'",
    ):
        toga.Image()


def test_empty_image():
    """If the image source is provided as None, an error is raised."""
    with pytest.raises(
        TypeError,
        match=r"Unsupported source type for Image",
    ):
        toga.Image(None)


def test_empty_image_explicit():
    """If src is explicitly provided as None, an error is raised."""
    with pytest.raises(
        TypeError,
        match=r"Unsupported source type for Image",
    ):
        toga.Image(src=None)


def test_invalid_input_format():
    """Trying to create an image with an invalid input should raise an error."""
    with pytest.raises(
        TypeError,
        match=r"Unsupported source type for Image",
    ):
        toga.Image(42)


def test_create_from_pil(app):
    """An image can be created from a PIL image."""
    with PIL.Image.open(ABSOLUTE_FILE_PATH) as pil_image:
        pil_image.load()
    toga_image = toga.Image(pil_image)

    assert isinstance(toga_image, toga.Image)
    assert toga_image.size == (144, 72)


def test_create_from_toga_image(app):
    """An image can be created from another Toga image."""
    toga_image = toga.Image(ABSOLUTE_FILE_PATH)
    toga_image_2 = toga.Image(toga_image)

    assert isinstance(toga_image_2, toga.Image)
    assert toga_image_2.size == (144, 72)


@pytest.mark.parametrize("kwargs", [{"data": BYTES}, {"path": ABSOLUTE_FILE_PATH}])
def test_deprecated_arguments(kwargs):
    with pytest.deprecated_call():
        toga.Image(**kwargs)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        # One positional, one keyword
        ((ABSOLUTE_FILE_PATH,), {"data": BYTES}),
        ((ABSOLUTE_FILE_PATH,), {"path": ABSOLUTE_FILE_PATH}),
        # Two keywords
        ((), {"data": BYTES, "path": ABSOLUTE_FILE_PATH}),
        # All three
        ((ABSOLUTE_FILE_PATH,), {"data": BYTES, "path": ABSOLUTE_FILE_PATH}),
    ],
)
def test_too_many_arguments(args, kwargs):
    """If multiple arguments are supplied, an error is raised."""
    with pytest.raises(
        TypeError,
        match=r"Received multiple arguments to constructor.",
    ):
        toga.Image(*args, **kwargs)


def test_dimensions(app):
    """The dimensions of the image can be retrieved."""
    image = toga.Image(RELATIVE_FILE_PATH)

    assert image.size == (144, 72)
    assert image.width == 144
    assert image.height == 72


def test_data(app):
    """The raw data of the image can be retrieved."""
    image = toga.Image(ABSOLUTE_FILE_PATH)

    # We can't guarantee the round-trip of image data,
    # but the data starts with a PNG header
    assert image.data.startswith(b"\x89PNG\r\n\x1a\n")

    # If we build a new image from the data, it has the same properties.
    from_data = toga.Image(image.data)
    assert from_data.width == image.width
    assert from_data.height == image.height


def test_image_save(tmp_path):
    """An image can be saved."""
    save_path = tmp_path / "save.png"
    image = toga.Image(BYTES)
    image.save(save_path)

    assert_action_performed_with(image, "save", path=save_path)


class ImageSubclass(toga.Image):
    pass


@pytest.mark.parametrize(
    "Class_1, Class_2",
    [
        (toga.Image, toga.Image),
        (toga.Image, ImageSubclass),
        (ImageSubclass, toga.Image),
        (ImageSubclass, ImageSubclass),
    ],
)
def test_as_format_toga(app, Class_1, Class_2):
    """as_format can successfully return a "copy" Image, with support for
    subclassing."""
    image_1 = Class_1(ABSOLUTE_FILE_PATH)
    image_2 = image_1.as_format(Class_2)

    assert isinstance(image_2, Class_2)
    assert image_2.size == (144, 72)


def test_as_format_pil(app):
    """as_format can successfully return a PIL image."""
    toga_image = toga.Image(ABSOLUTE_FILE_PATH)
    pil_image = toga_image.as_format(PIL.Image.Image)
    assert isinstance(pil_image, PIL.Image.Image)
    assert pil_image.size == (144, 72)


@pytest.mark.parametrize("ImageClass", [CustomImage, CustomImageSubclass])
def test_create_from_custom_class(app, ImageClass):
    """toga.Image can be created from custom type."""
    custom_image = ImageClass()
    toga_image = toga.Image(custom_image)
    assert isinstance(toga_image, toga.Image)
    assert toga_image.size == (144, 72)


@pytest.mark.parametrize("ImageClass", [CustomImage, CustomImageSubclass])
def test_as_format_custom_class(app, ImageClass):
    """as_format can successfully return a registered custom image type."""
    toga_image = toga.Image(ABSOLUTE_FILE_PATH)
    custom_image = toga_image.as_format(ImageClass)
    assert isinstance(custom_image, ImageClass)
    assert custom_image.size == (144, 72)


def test_disabled_image_plugin(app):
    """Disabled image plugin shouldn't be available."""
    assert DisabledImageConverter not in toga.Image._converters()


# None is same as supplying nothing; also test a random unrecognized class
@pytest.mark.parametrize("arg", [None, toga.Button])
def test_as_format_invalid_input(app, arg):
    """An unsupported format raises an error."""
    toga_image = toga.Image(ABSOLUTE_FILE_PATH)

    with pytest.raises(TypeError, match=r"Unknown conversion format for Image:"):
        toga_image.as_format(arg)
