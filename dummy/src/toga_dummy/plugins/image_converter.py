from pathlib import Path

import toga


class CustomImage:
    pass


class CustomImageSubclass(CustomImage):
    pass


image_class = CustomImage


def convert_from_format(image_in_format):
    return (Path(__file__).parent.parent / "resources/sample.png").read_bytes()


def convert_to_format(data, image_class):
    image = image_class()
    image.size = toga.Image(data).size
    return image
