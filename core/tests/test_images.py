from pathlib import Path

import PIL.Image
import pytest

import toga
from toga_dummy.utils import assert_action_performed_with

RELATIVE_FILE_PATH = Path("resources/toga.png")
ABSOLUTE_FILE_PATH = Path(toga.__file__).parent / "resources/toga.png"


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
    """An image can be constructed from a file"""
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
    """If a file image source doesn't exist, an error is raised"""
    with pytest.raises(FileNotFoundError):
        toga.Image(*args, **kwargs)


BYTES = bytes([1])


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        # Empty string
        ((BYTES,), {}),
        ((), {"src": BYTES}),
        ((), {"data": BYTES}),
    ],
)
def test_create_from_bytes(args, kwargs):
    """An image can be constructed from data"""
    image = toga.Image(*args, **kwargs)

    # Image is bound
    assert image._impl is not None
    # impl/interface round trips
    assert image._impl.interface == image

    # Image was constructed with data
    assert_action_performed_with(image, "load image data", data=BYTES)


def test_not_enough_arguments():
    with pytest.raises(
        ValueError,
        match=r"No image source supplied.",
    ):
        toga.Image(None)


def test_invalid_input_format():
    """Trying to create an image with an invalid input should raise an error"""
    with pytest.raises(
        TypeError,
        match=r"Unsupported source type for Image",
    ):
        toga.Image(42)


def test_create_from_pil(app):
    """An image can be created from a PIL image"""
    pil_img = PIL.Image.open(ABSOLUTE_FILE_PATH)
    toga_img = toga.Image(pil_img)

    assert isinstance(toga_img, toga.Image)


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
    """If multiple arguments are supplied, an error is raised"""
    with pytest.raises(
        ValueError,
        match=r"Received multiple arguments to constructor.",
    ):
        toga.Image(*args, **kwargs)


def test_dimensions(app):
    """The dimensions of the image can be retrieved"""
    image = toga.Image(RELATIVE_FILE_PATH)

    assert image.size == (60, 40)
    assert image.width == 60
    assert image.height == 40


def test_data(app):
    """The raw data of the image can be retrieved."""
    image = toga.Image(ABSOLUTE_FILE_PATH)
    assert image.data == b"pretend this is PNG image data"


def test_image_save(tmp_path):
    """An image can be saved"""
    save_path = tmp_path / "save.png"
    image = toga.Image(BYTES)
    image.save(save_path)

    assert_action_performed_with(image, "save", path=save_path)


def test_as_format_pil(app):
    """as_format can successfully return a PIL image"""
    toga_img = toga.Image(ABSOLUTE_FILE_PATH)
    # The dummy backend only supplies toy data, but this verifies that it is being
    # fed to PIL.Image.open
    with pytest.raises(PIL.UnidentifiedImageError):
        toga_img.as_format(PIL.Image.Image)


# None is same as supplying nothing; also test a random unrecognized class
@pytest.mark.parametrize("arg", [None, toga.Button])
def test_as_format_invalid_input(app, arg):
    """An unsupported format raises an error"""
    toga_img = toga.Image(ABSOLUTE_FILE_PATH)

    with pytest.raises(TypeError, match=r"Unknown conversion format for Image:"):
        toga_img.as_format(arg)
