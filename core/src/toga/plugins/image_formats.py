from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.images import BytesLikeT

# Presumably, other converter plugins will be included with, or only installed
# alongside, the packages they're for. But since this is provided in Toga, we need to
# check if Pillow is actually installed, and disable this plugin otherwise.
try:
    import PIL.Image

    PIL_imported = True  # pragma: no-cover-if-missing-PIL

except ImportError:  # pragma: no-cover-if-PIL-installed
    PIL_imported = False


class PILConverter:
    image_class = PIL.Image.Image if PIL_imported else None

    @staticmethod
    def convert_from_format(image_in_format: PIL.Image.Image) -> bytes:
        buffer = BytesIO()
        image_in_format.save(buffer, format="png", compress_level=0)
        return buffer.getvalue()

    @staticmethod
    def convert_to_format(
        data: BytesLikeT,
        image_class: type[PIL.Image.Image],
    ) -> PIL.Image.Image:
        # PIL Images aren't designed to be subclassed, so no implementation is necessary
        # for a supplied format.
        buffer = BytesIO(data)
        with PIL.Image.open(buffer) as pil_image:
            pil_image.load()
        return pil_image
