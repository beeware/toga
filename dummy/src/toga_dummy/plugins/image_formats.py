from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import toga

if TYPE_CHECKING:
    from toga.images import BytesLikeT


class CustomImage:
    pass


class CustomImageSubclass(CustomImage):
    pass


class CustomImageConverter:
    image_class = CustomImage

    @staticmethod
    def convert_from_format(image_in_format: CustomImage):
        return (Path(__file__).parent.parent / "resources/sample.png").read_bytes()

    @staticmethod
    def convert_to_format(
        data: BytesLikeT,
        image_class: type[CustomImage],
    ) -> CustomImage:
        image = image_class()
        image.size = toga.Image(data).size
        return image


# With image_class set to None, this converter shouldn't be added to the list of
# available converters. This simulates what the PIL plugin does if PIL isn't installed.
class DisabledImageConverter:
    image_class = None

    @staticmethod
    def convert_from_format(image_in_format: Any):
        raise Exception("Converter should be disabled")

    @staticmethod
    def convert_to_format(
        data: BytesLikeT,
        image_class: type[Any],
    ) -> Any:
        raise Exception("Converter should be disabled")
