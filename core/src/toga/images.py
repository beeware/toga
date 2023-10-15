from __future__ import annotations

from typing import Any

from pathlib import Path

import toga
from toga.platform import get_platform_factory

from io import BytesIO
import time, os

try:
    from PIL import Image as PIL_Image
    PIL_ImportError_Message = None
except ImportError as e:
    PIL_Image = None
    PIL_ImportError_Message = e
class Image:
    def __init__(
        self,
        path: str | None | Path = None,
        *,
        data: bytes | None = None,
        pil_image: Any | None = None,
    ):
        """Create a new image.

        An image must be one of ``path``, ``data`` or ``pil_image``

        :param path: Path to the image to load. This can be specified as a string, or as
            a :any:`pathlib.Path` object. The path can be an absolute file system path,
            or a path relative to the module that defines your Toga application class.
        :param data: A bytes object with the contents of an image in a supported format.
        :param pil_image: PIL.Image object created from an image of a supported format.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the path or data cannot be loaded as an image.
        :raises TypeError: If pil_image is provided but the type of the object is not PIL.Image
        """
        # At first we will create a list with these three variable, then count how many None is in that list.
        # If the number of None is 1 -> raises ValueError. One and only One of the three variables must be set but here two of them are set
        # If the number of None is 3 -> raises ValueError. One and only One of the three variables must be set but here none of them are set 
        # If the number of None is 2 -> Ok. Check the validity of the value of that non-None variable
        none_count = [path, data, pil_image].count(None)
        if none_count != 2:
            raise ValueError("One and Only one of the three args (path, data, pil_image) must be set.")
        # checking validity of the arg(one of the three)
        if path is not None:
            if isinstance(path, Path):
                self.path = path
            else:
                self.path = Path(path)
            self.data = None
            self.pil_image = None
        if data is not None:
            self.data = data
            self.path = None
            self.pil_image = None
        if pil_image is not None:
            if PIL_Image == None:
                raise ImportError(PIL_ImportError_Message)
            if not PIL_Image.isImageType(pil_image):
                raise TypeError("pil_image is not a PIL.Image type.")
            self.pil_image = pil_image
            self.data = None
            self.path = None


        self.factory = get_platform_factory()
        if self.data is not None:
            self._impl = self.factory.Image(interface=self, data=self.data)
        if self.path is not None:
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)
        if self.pil_image is not None:
            img_buffer = BytesIO()
            self.pil_image.save(img_buffer, format=self.pil_image.format)
            img_buffer.seek(0)
            self._impl = self.factory.Image(interface=self, data=img_buffer.read())




    @property
    def width(self) -> int:
        """The width of the image, in pixels."""
        return self._impl.get_width()

    @property
    def height(self) -> int:
        """The height of the image, in pixels."""
        return self._impl.get_height()

    def save(self, path: str | Path):
        """Save image to given path.

        The file format of the saved image will be determined by the extension of
        the filename provided (e.g ``path/to/mypicture.png`` will save a PNG file).

        :param path: Path where to save the image.
        """
        self._impl.save(path)
    
    def as_format(self, format: Any|None=None):
        """
        get the image as specified format if supported
        :param format: None or A supported type of Image
        Supported types are `PIL.Image.Image`,
        :returns: toga.Image if format is None, or the specified format if the format is supported
        ```
        from PIL import Image
        pil_image = toga_image.as_format(Image.Image)
        ```
        """
        if format == None:
            return self
        elif PIL_Image != None and format == PIL_Image.Image:
            # saving into temporary file
            unique_time = str(time.time())
            temp_file = f"._toga_Image_as_format_PIL_Image_{unique_time}_"
            temp_file_path = os.path.join(toga.App.app.paths.app, temp_file)
            self.save(temp_file_path)
            # creating PIL.Image.Image from temporary file
            pil_image = PIL_Image.open(temp_file_path)
            # deleting the temporary file
            os.remove(temp_file_path)

            return pil_image
        else:
            raise TypeError(f"Unknown conversion format: {format}")

