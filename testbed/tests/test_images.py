import io
import os
import re
import shutil
from importlib import import_module

import pytest
from PIL import Image as PIL_Image, ImageDraw as PIL_ImageDraw

import toga


def image_probe(app, image):
    module = import_module("tests_backend.images")
    return getattr(module, "ImageProbe")(app, image)


async def test_local_image(app):
    "An image can be specified by filename"
    image = toga.Image("resources/sample.png")
    assert image.width == 144
    assert image.height == 72


async def test_bad_image_file(app):
    "If a file isn't a loadable image, an error is raised"
    with pytest.raises(
        ValueError,
        match=rf"Unable to load image from {re.escape(__file__)}",
    ):
        toga.Image(__file__)


async def test_data_image(app):
    "An image can be constructed from data"
    # Generate an image using pillow
    pil_image = PIL_Image.new("RGBA", size=(110, 30))
    draw_context = PIL_ImageDraw.Draw(pil_image)
    draw_context.text((20, 10), "Hello World", fill="green")

    buffer = io.BytesIO()
    pil_image.save(buffer, format="png", compress_level=0)

    # Construct a Toga image.
    image = toga.Image(data=buffer.getvalue())

    assert image.width == 110
    assert image.height == 30

    # Construct a second image from the first image's data
    image2 = toga.Image(data=image.data)

    assert image2.width == 110
    assert image2.height == 30


async def test_bad_image_data(app):
    "If data isn't a valid image, an error is raised"
    with pytest.raises(
        ValueError,
        match=r"Unable to load image from data",
    ):
        toga.Image(data=b"Not an image")


async def test_save(app):
    """An image can be saved."""
    orig_image = toga.Image("resources/sample.png")
    probe = image_probe(app, orig_image)
    assert orig_image.width == 144
    assert orig_image.height == 72

    try:
        output_folder = app.paths.data / "images"
        output_folder.mkdir(parents=True, exist_ok=True)
        for i, extension in enumerate(
            [
                "",  # No extension
                ".unknown",  # Something that won't exist
                ".png",
                ".PNG",  # Check upper case
                ".jpg",
                ".jpeg",
                ".gif",
                ".bmp",
                ".tiff",
            ]
        ):
            filename = output_folder / f"image-{os.getpid()}-{i}{extension}"

            if probe.supports_extension(extension):
                orig_image.save(filename)
                await probe.redraw(f"Saving {filename}")

                assert filename.exists()
                new_image = toga.Image(filename)
                assert new_image.width == orig_image.width
                assert new_image.height == orig_image.height
            else:
                with pytest.raises(
                    ValueError,
                    match=f"Don't know how to save image of type '{extension}'",
                ):
                    orig_image.save(filename)

                await probe.redraw(f"Doesn't support files of type {extension!r}")

                assert not filename.exists()

    finally:
        if output_folder.exists():
            try:
                shutil.rmtree(output_folder)
            except PermissionError:
                # On Winforms, Python.net has open file references to the
                # `new_image` instances created to validate that the image was
                # successfully saved. These will be garbage collected
                # eventually, but there's non way to force the issue for test
                # cleanup. The files will be cleaned up the next time the test
                # suite is run; and the files have a PID in them to ensure that
                # they're unique across test runs.
                pass
