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
        src:str|Path|bytes|PIL_Image.Image|None=None,
        *,
        path: str | None | Path = None,
        data: bytes | None = None,
    ):
        """Create a new image.

        :param src: path, data or pillow object of the image to load
        :param path: Path to the image to load. This can be specified as a string, or as
            a :any:`pathlib.Path` object. The path can be an absolute file system path,
            or a path relative to the module that defines your Toga application class.
        :param data: A bytes object with the contents of an image in a supported format.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the path or data cannot be loaded as an image.
        """
        none_count = [src, path, data].count(None)
        if none_count != 2:
            raise ValueError("One and Only one of the three parameters (src, path, data) have to be set.")
        
        if src is not None:
            if isinstance(src, str) or isinstance(src, Path):
                path = src
                src = None
            elif isinstance(src, bytes):
                data = src
                src = None
            elif PIL_Image is not None and isinstance(src, PIL_Image.Image):
                img_buffer = BytesIO()
                src.save(img_buffer, format=src.format)
                img_buffer.seek(0)
                data = img_buffer.read()
                src = None
            else:
                raise TypeError("Unsupported source type for image.")
                
        if path is not None:
            if isinstance(path, Path):
                self.path = path
            else:
                self.path = Path(path)
            self.data = None
        if data is not None:
            self.data = data
            self.path = None


        self.factory = get_platform_factory()
        if self.data is not None:
            self._impl = self.factory.Image(interface=self, data=self.data)
        if self.path is not None:
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)




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
    
    def as_format(self, format: Any):
        """
        Convert the image to format specified.
        Supported formats are: Pillow Object,
        
        To convert the image to Pillow object
        ```
        from PIL import Image as PIL_Image
        pil_image = toga_image.as_format(PIL_Image.Image)
        toga_img = toga_image.as_format(toga.Image)
        ```
        """
        if PIL_Image != None and format == PIL_Image.Image:
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

