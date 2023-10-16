from pathlib import Path
from io import BytesIO
from PIL import Image as PIL_Image

import pytest

import toga
from toga_dummy.utils import assert_action_performed_with

RELATIVE_FILE_PATH = Path("resources") / "toga.png"
ABSOLUTE_FILE_PATH = Path(toga.__file__).parent / "resources" / "toga.png"


@pytest.fixture
def app():
    return toga.App("Images Test", "org.beeware.toga.images")


@pytest.mark.parametrize(
    "args, kwargs",
    [
        # Fully qualified path
        ((ABSOLUTE_FILE_PATH,), {}),
        ((), dict(path=ABSOLUTE_FILE_PATH)),
        # Fully qualified string
        ((f"{ABSOLUTE_FILE_PATH}",), {}),
        ((), dict(path=f"{ABSOLUTE_FILE_PATH}")),
        # Relative path
        ((RELATIVE_FILE_PATH,), {}),
        ((), dict(path=RELATIVE_FILE_PATH)),
        # Relative string
        ((f"{RELATIVE_FILE_PATH}",), {}),
        ((), dict(path=f"{RELATIVE_FILE_PATH}")),
    ],
)
def test_create_from_file(app, args, kwargs):
    "If an file image source doesn't exist, an error is raised"
    image = toga.Image(*args, **kwargs)

    # Image is bound
    assert image._impl is not None
    # impl/interface round trips
    assert image._impl.interface == image

    # The image's path is fully qualified
    assert image._impl.interface.path == ABSOLUTE_FILE_PATH


MISSING_ABSOLUTE_PATH = Path.home() / "does" / "not" / "exist" / "image.jpg"
MISSING_RELATIVE_PATH = Path("does") / "not" / "exist" / "image.jpg"


@pytest.mark.parametrize(
    "args, kwargs",
    [
        # Empty string
        (("",), {}),
        ((), dict(path="")),
        # Absolute path
        ((MISSING_ABSOLUTE_PATH,), {}),
        ((), dict(path=MISSING_ABSOLUTE_PATH)),
        # Absolute string
        ((f"{MISSING_ABSOLUTE_PATH}",), {}),
        ((), dict(path=f"{MISSING_ABSOLUTE_PATH}")),
        # Relative path
        ((MISSING_RELATIVE_PATH,), {}),
        ((), dict(path=f"{MISSING_RELATIVE_PATH}")),
        # Relative string
        ((f"{MISSING_RELATIVE_PATH}",), {}),
        ((), dict(path=f"{MISSING_RELATIVE_PATH}")),
    ],
)
def test_create_with_non_existent_file(app, args, kwargs):
    "If an file image source doesn't exist, an error is raised"
    with pytest.raises(FileNotFoundError):
        toga.Image(*args, **kwargs)


def test_bytes():
    "An image can be constructed from data"
    data = bytes([1])
    image = toga.Image(data=data)

    # Image is bound
    assert image._impl is not None
    # impl/interface round trips
    assert image._impl.interface == image

    # Image was constructed with data
    assert_action_performed_with(image, "load image data", data=data)


def test_not_enough_arguments():
    with pytest.raises(
        ValueError,
        match=r"Either path or data must be set.",
    ):
        toga.Image(None)


def test_too_many_arguments():
    with pytest.raises(
        ValueError,
        match=r"Only either path or data can be set.",
    ):
        toga.Image(path="/image.png", data=bytes([1]))


def test_dimensions():
    "The dimensions of the image can be retrieved"

    image = toga.Image(path="resources/toga.png")

    assert image.width == 60
    assert image.height == 40


def test_image_save():
    "An image can be saved"
    save_path = Path("/path/to/save.png")
    image = toga.Image(path=ABSOLUTE_FILE_PATH)

    image.save(save_path)
    assert_action_performed_with(image, "save", path=save_path)

def test_pil_support():
    pil_img = PIL_Image.open("resources/toga.png")
    toga_img_from_pil_img = toga.Image(pil_img)

    assert toga_img_from_pil_img.width == 60, "PIL support is faulty"
    assert toga_img_from_pil_img.height == 40, "PIL support is faulty"

def test_as_format():
    img = toga.Image("resources/toga.png")
    img2 = img.as_format()
    assert img == img2, "Image.as_format should return toga.Image when nothing is provided as arg, but failed"

    pil_img = img.as_format(PIL_Image.Image)
    assert isinstance(pil_img, PIL_Image.Image)
    assert pil_img.size == (60, 40)

test_image_path = "resources/toga.png"
@pytest.mark.parametrize("unified_image_source",[
    test_image_path, #normal string paths
    Path(test_image_path), #pathlib.Path
    open(test_image_path, "rb"), #BufferedReader
    open(test_image_path, "rb").read(),#bytes
    BytesIO(open(test_image_path, "rb").read()), #BytesIO
    PIL_Image.open(test_image_path), #PIL_Image.Image
])

def test_unified_source(unified_image_source):
    image = toga.Image(unified_image_source)
    assert image is not None and image.width is not None and image.height is not None

