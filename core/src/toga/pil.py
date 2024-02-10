from io import BytesIO

# Presumably, other converter plugins will be included with, or only installed
# alongside, the packages they're for. But since this is provided in Toga, we need to
# check if Pillow is actually installed, and disable this plugin otherwise.
try:
    import PIL.Image

    image_class = PIL.Image.Image

except ImportError:  # pragma: no cover
    image_class = None


def convert_from_format(image_in_format):
    buffer = BytesIO()
    image_in_format.save(buffer, format="png", compress_level=0)
    return buffer.getvalue()


def convert_to_format(data, image_class=None):
    # PIL Images aren't designed to be subclassed, so no implementation is necessary for
    # a supplied format.
    buffer = BytesIO(data)
    with PIL.Image.open(buffer) as pil_image:
        pil_image.load()
    return pil_image
