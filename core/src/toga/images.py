from __future__ import annotations

from pathlib import Path

import toga
from toga.platform import get_platform_factory


class Image:
    def __init__(
        self,
        path: str | None | Path = None,
        *,
        data: bytes | None = None,
        pil_image: PIL.Image | None = None,
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
        #--patch-start:@github/dr-gavitron
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
            try:
                from PIL import Image as _PIL_Image_Module_
            except ImportError as e:
                print("Pillow is required as pil_image is set to a PIL.Image type")
                raise ImportError(e)
            #type checking
            if not _PIL_Image_Module_.isImageType(pil_image):
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
            #What we will do: save the pil_image into a temporary file then load raw byte data
            #from that file, then use the bytes to create self._impl, finally delete the temp file

            # creating an unique name for the temporary file
            from time import time as _time_time
            import os as _os
            unique_time = str(_time_time())
            temp_file = f"_PIL_temp_img_file_{unique_time}_"
            temp_file_path = toga.App.app.paths.app
            while temp_file in _os.listdir(temp_file_path):
                temp_file+="1_"
            complete_temp_path = _os.path.join(temp_file_path, temp_file)

            # saving the pil_image in the temporary file
            self.pil_image.save(complete_temp_path)

            #loading the raw bytes of the image into the memory from the temporary file
            with open(complete_temp_path, "rb") as _file:
                raw_image_data = _file.read()

            #passing the bytes of the image to create _impl
            self._impl = self.factory.Image(interface=self, data=raw_image_data)

            #finally delete the temporary file from the storage
            _os.remove(temp_file_path)



        #--patch-end
        '''
        if path is None and data is None:
            raise ValueError("Either path or data must be set.")
        if path is not None and data is not None:
            raise ValueError("Only either path or data can be set.")
        if path is not None:
            if isinstance(path, Path):
                self.path = path
            else:
                self.path = Path(path)
            self.data = None
        else:
            self.path = None
            self.data = data

        self.factory = get_platform_factory()
        if self.data is not None:
            self._impl = self.factory.Image(interface=self, data=self.data)
        else:
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)
        '''

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
